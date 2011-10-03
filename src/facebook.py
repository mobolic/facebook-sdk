#!/usr/bin/env python
#
# Copyright 2010 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Python client library for the Facebook Platform.

This client library is designed to support the Graph API and the official
Facebook JavaScript SDK, which is the canonical way to implement
Facebook authentication. Read more about the Graph API at
http://developers.facebook.com/docs/api. You can download the Facebook
JavaScript SDK at http://github.com/facebook/connect-js/.

If your application is using Google AppEngine's webapp framework, your
usage of this module might look like this:

    user = facebook.get_user_from_cookie(self.request.cookies, key, secret)
    if user:
        graph = facebook.GraphAPI(user["access_token"])
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")

"""

import hashlib
import hmac
import string
import urllib
import random
import mimetypes
import httplib
import json
import urllib2
import base64
import logging
import urlparse

class GraphAPI(object):
    """A client for the Facebook Graph API.

    See http://developers.facebook.com/docs/api for complete documentation
    for the API.

    The Graph API is made up of the objects in Facebook (e.g., people, pages,
    events, photos) and the connections between them (e.g., friends,
    photo tags, and event RSVPs). This client provides access to those
    primitive types in a generic way. For example, given an OAuth access
    token, this will fetch the profile of the active user and the list
    of the user's friends:

       graph = facebook.GraphAPI(access_token)
       user = graph.get_object("me")
       friends = graph.get_connections(user["id"], "friends")

    You can see a list of all of the objects and connections supported
    by the API at http://developers.facebook.com/docs/reference/api/.

    You can obtain an access token via OAuth or by using the Facebook
    JavaScript SDK. See http://developers.facebook.com/docs/authentication/
    for details.

    If you are using the JavaScript SDK, you can use the
    get_user_from_cookie() method below to get the OAuth access token
    for the active user from the cookie saved by the SDK.
    """

    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_object(self, id, **args):
        """Fetchs the given object from the graph."""
        return self.request(id, args)

    def get_objects(self, ids, **args):
        """Fetchs all of the given object from the graph.

        We return a map from ID to object. If any of the IDs are invalid,
        we raise an exception.
        """
        args["ids"] = ",".join(ids)
        return self.request("", args)

    def get_connections(self, id, connection_name, **args):
        """Fetchs the connections for given object."""
        return self.request(id + "/" + connection_name, args)

    def put_object(self, parent_object, connection_name, **data):
        """Writes the given object to the graph, connected to the given parent.

        For example,

            graph.put_object("me", "feed", message="Hello, world")

        writes "Hello, world" to the active user's wall. Likewise, this
        will comment on a the first post of the active user's feed:

            feed = graph.get_connections("me", "feed")
            post = feed["data"][0]
            graph.put_object(post["id"], "comments", message="First!")

        See http://developers.facebook.com/docs/api#publishing for all of
        the supported writeable objects.

        Most write operations require extended permissions. For example,
        publishing wall posts requires the "publish_stream" permission. See
        http://developers.facebook.com/docs/authentication/ for details about
        extended permissions.
        """
        assert self.access_token, "Write operations require an access token"
        return self.request(parent_object + "/" + connection_name, post_args=data)

    def put_wall_post(self, message, attachment=None, profile_id="me"):
        """Writes a wall post to the given profile's wall.

        We default to writing to the authenticated user's wall if no
        profile_id is specified.

        attachment adds a structured attachment to the status message being
        posted to the Wall. It should be a dictionary of the form:

            {"name": "Link name"
             "link": "http://www.example.com/",
             "caption": "{*actor*} posted a new review",
             "description": "This is a longer description of the attachment",
             "picture": "http://www.example.com/thumbnail.jpg"}

        """
        if not attachment:
            attachment = {}
        return self.put_object(profile_id, "feed", message=message, **attachment)

    def put_event(self, id=None, **data):
        """Creates an event with a picture.

        We accept the params as per http://developers.facebook.com/docs/reference/api/event
        However, we also accept a picture param, which should point to a URL for
        the event image.

        """
        files = {}
        if 'picture' in data:
            with urllib.urlopen(data['picture']) as file:
                files['picture'] = file.read()
            del data['picture']

        path = "me/events" if not id else str(id)
        return self.multipart_request(path, post_args=data, files=files)

    def put_comment(self, object_id, message):
        """Writes the given comment on the given post."""
        return self.put_object(object_id, "comments", message=message)

    def put_like(self, object_id):
        """Likes the given post."""
        return self.put_object(object_id, "likes")

    def delete_object(self, id):
        """Deletes the object with the given ID from the graph."""
        return self.request(id, post_args={"method": "delete"})

    def put_photo(self, image, message=None, album_id=None, **kwargs):
        """Uploads an image using multipart/form-data
        image=File like object for the image
        message=Caption for your image
        album_id=None posts to /me/photos which uses or creates and uses
        an album for your application.
        """
        object_id = album_id or "me"
        #it would have been nice to reuse self.request; but multipart is messy in urllib
        post_args = {
				  'access_token': self.access_token,
				  'source': image,
				  'message': message
        }
        post_args.update(kwargs)
        content_type, body = self._encode_multipart_form(post_args)
        req = urllib2.Request("https://graph.facebook.com/%s/photos" % object_id, data=body)
        req.add_header('Content-Type', content_type)
        try:
            data = urllib2.urlopen(req).read()
        #For Python 3 use this:
        #except urllib2.HTTPError as e:
        except urllib2.HTTPError, e:
            data = e.read() # Facebook sends OAuth errors as 400, and urllib2 throws an exception, we want a GraphAPIError
        try:
            response = json.loads(data)
            if response and response.get("error"):
                raise GraphAPIError(response["error"].get("code", 1),
                                    response["error"]["message"])
        except ValueError:
            response = data

        return response

    # based on: http://code.activestate.com/recipes/146306/
    def _encode_multipart_form(self, fields):
        """Fields are a dict of form name-> value
        For files, value should be a file object.
        Other file-like objects might work and a fake name will be chosen.
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.items():
            logging.debug("Encoding %s, (%s)%s" % (key, type(value), value))
            if not value:
                continue
            L.append('--' + BOUNDARY)
            if hasattr(value, 'read') and callable(value.read):
                filename = getattr(value,'name','%s.jpg' % key)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
                L.append('Content-Type: image/jpeg')
                value = value.read()
                logging.debug(type(value))
            else:
                L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            if isinstance(value, unicode):
                logging.debug("Convert to ascii")
                value = value.encode('ascii')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def request(self, path, args=None, post_args=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        post_data = None if post_args is None else urllib.urlencode(post_args)
        graph_api = "https://graph.facebook.com/{0}?{1}"
        request = urllib2.Request(graph_api.format(path, urllib.urlencode(args)), data=post_data)

        try:
            file = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            response = json.loads( e.read() )
            raise GraphAPIError(response["error"]["type"],
                    response["error"]["message"])

        try:
            fileInfo = file.info()
            if fileInfo.maintype == 'text':
                response = file.read()
                try:
                    response = json.loads(response)
                except ValueError:
                    return response
            elif fileInfo.maintype == 'image':
                mimetype = fileInfo['content-type']
                response = {
                    "data": file.read(),
                    "mime-type": mimetype,
                    "url": file.url,
                }
            else:
                raise GraphAPIError('Response Error', 'Maintype was not text or image')
        finally:
            file.close()
            
        if response and isinstance(response, dict) and response.get("error"):
            raise GraphAPIError(response["error"]["type"],
                                response["error"]["message"])
        return response

    def api_request(self, path, args=None, post_args=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        if post_args is not None:
            post_args["format"] = "json-strings"
        else:
            args["format"] = "json-strings"
        post_data = None if post_args is None else urllib.urlencode(post_args)

        encoded_args = urllib.urlencode(args)
        graph_api = "https://api.facebook.com/method/{0}?{1}"
        request = urllib2.Request(graph_api.format(path,encoded_args), data=post_data)
        
        with urllib2.urlopen(request) as file:
            response = json.loads(file.read())

        if isinstance(response, dict) and response.get("error"):
            raise GraphAPIError(response["error"]["type"],
                                response["error"]["message"])
        return response

    def multipart_request(self, path, args=None, post_args=None, files=None):
        """Request a given path in the Graph API with multipart support.

        If post_args or files is given, we send a POST multipart request.

        files is a dict of {'filename.ext', 'value'} of files to upload.
        """
        def __encode_multipart_data(post_args, files):
            boundary = ''.join(random.choice(string.ascii_letters) for i in xrange(31))

            def get_content_type(filename):
                return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

            def encode_field(field_name, value):
                return ('--' + boundary,
                        'Content-Disposition: form-data; name="%s"' % field_name,
                        '', str(value))

            def encode_file(filename, value):
                return ('--' + boundary,
                        'Content-Disposition: form-data; filename="%s"' % (filename, ),
                        'Content-Type: %s' % get_content_type(filename),
                        '', value)

            lines = []
            for (field_name, value) in post_args.items():
                lines.extend(encode_field(field_name, value))
            for (filename, value) in files.items():
                lines.extend(encode_file(filename, value))
            lines.extend(('--%s--' % boundary, ''))
            body = '\r\n'.join(lines)

            headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
                       'content-length': str(len(body))}

            return body, headers

        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token

        path = path + "?" + urllib.urlencode(args)
        connection = httplib.HTTPSConnection("graph.facebook.com")
        method = "POST" if post_args or files else "GET"
        connection.request(method, path,
                            *__encode_multipart_data(post_args, files))
        http_response = connection.getresponse()
        try:
            response = json.loads(http_response.read())
        finally:
            http_response.close()
            connection.close()
        if isinstance(response, dict) and response.get("error"):
            raise GraphAPIError(response["error"]["type"],
                                response["error"]["message"])
        return response


    def fql(self, query, args=None, post_args=None):
        """FQL query.
        Two reasons to have this method:
        1. Graph api does not expose some info fields of a user, e.g.
            a user's networks/affiliations, we have to fall back to old api.
        2. FQL is a strong tool.
        Example query: "SELECT affiliations FROM user WHERE uid = me()"
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        post_data = None if post_args is None else urllib.urlencode(post_args)

        args["query"] = query
        args["format"]="json"
        file = urllib2.urlopen("https://api.facebook.com/method/fql.query?" +
                              urllib.urlencode(args), post_data)
        try:
            content  = file.read()
            response = json.loads(content)
            #Return a list if success, return a dictionary if failed
            if type(response) is dict and "error_code" in response:
                raise GraphAPIError(response["error_code"],response["error_msg"])
        except Exception, e:
            raise e
        finally:
            file.close()

        return response


class GraphAPIError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type

class FQLAPI(object):
    """
    A client for the Facebook FQL API.

    See http://developers.facebook.com/docs/reference/fql/ for complete documentation
    for the API.

    The Graph API is made up of the objects in Facebook (e.g., people, pages,
    events, photos) and the connections between them (e.g., friends,
    photo tags, and event RSVPs). This client provides access to those
    primitive types in an advanced way. For example, given an OAuth access
    token, this will fetch the profile of the active user and list the user's
    friend's profile pictures.

        graph = facebook.GraphAPI(access_token)
        user = graph.get_object("me")
        fql = facebook.FQLAPI(access_token)
        friends = fql.query("SELECT pic_small FROM profile where id in (SELECT uid2 from friend where uid1 = " + user["id"] + ")")


    You can see a list of all of the objects and connections supported
    by the API at http://developers.facebook.com/docs/reference/fql/.

    You can obtain an access token via OAuth or by using the Facebook
    JavaScript SDK. See http://developers.facebook.com/docs/authentication/
    for details.

    If you are using the JavaScript SDK, you can use the
    get_user_from_cookie() method below to get the OAuth access token
    for the active user from the cookie saved by the SDK.
    """

    def __init__(self, access_token):
        self.access_token = access_token

    def query(self, query):
        """ Performs a FQL query on Facebook. Just a wrapper around the `request`
        method below. """
        return self.request(query)

    def request(self, query):
        """ Performs the given query on Facebook or raises an `FQLAPIError` """

        file = urllib2.urlopen('https://api.facebook.com/method/fql.query?access_token=%s&format=json&query=%s' % (
            urllib.quote_plus(self.access_token), urllib.quote_plus(query)))
        try:
            response = json.loads(file.read())
        finally:
            file.close()

        if isinstance(response, dict) and response.get('error_code'):
            raise FQLAPIError(response['error_code'], response['error_msg'])

        return response


class FQLAPIError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type


def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))


def parse_signed_request(signed_request, secret):
    """Parses a signed_request and validates the signature.

    See https://developers.facebook.com/docs/authentication/signed_request/

    Based on http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas
    """
    if not signed_request: return None

    logger = logging.getLogger('facebook')
    try:
        encoded_sig, payload = signed_request.split('.', 1)
    except ValueError:
        logger.error("Not a valid signed_request.")
        return None

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        logger.error("Unknown algorithm. Expected HMAC-SHA256")
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig == expected_sig:
        return data
    else:
        logger.error("Bad Signed JSON signature!")
        return None

def get_user_access_token(signed_request, client_id, client_secret):
    """Return access_token from signed_request or using code via Oauth 2.0.

    See:
    - https://developers.facebook.com/docs/authentication/
    - https://developers.facebook.com/docs/authentication/signed_request/
    - https://github.com/facebook/php-sdk/blob/master/src/base_facebook.php

    """
    if signed_request.get('oauth_token', False):
        return signed_request['oauth_token']

    code = signed_request.get('code')
    if not code:
        return None

    try:
        u = urllib2.urlopen(
            'https://graph.facebook.com/oauth/access_token',
            data=urllib.urlencode({
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': '',
            })
        )
    except urllib2.HTTPError, e:
        response = json.load(e)
        if isinstance(response, dict) and 'error' in response:
            raise GraphAPIError(response['error']['type'], response['error']['message'])
        return response

    response = u.read()
    data = urlparse.parse_qs(response)
    try:
        return data['access_token'][-1]
    except KeyError:
        return None

def get_user_from_cookie(cookies, app_id, app_secret):
    """Parses the cookie set by the official Facebook JavaScript SDK.

    cookies should be a dictionary-like object mapping cookie names to
    cookie values.

    If the user is logged in via Facebook, we return a dictionary with the
    keys "uid" and "access_token". The former is the user's Facebook ID,
    and the latter can be used to make authenticated requests to the Graph API.
    If the user is not logged in, we return None.

    Download the official Facebook JavaScript SDK at
    http://github.com/facebook/connect-js/. Read more about Facebook
    authentication at http://developers.facebook.com/docs/authentication/.
    """
    signed_request = cookies.get("fbsr_%s" % (app_id, ), "")
    if not signed_request: return None
    return parse_signed_request(signed_request, app_secret)
