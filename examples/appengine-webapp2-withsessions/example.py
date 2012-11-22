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

"""
An AppEngine application that demonstrates how to use webapp2's sessions with Facebook for login.

1. Make sure you add a copy of facebook.py (from python-sdk/src/) into this
directory so it can be imported.
2. Don't forget to tick Login With Facebook on your facebook app's dashboard
3. Place a random, unguessable string as a session secret below in config dict.
4. Fill app id and app secret.
"""

import facebook
import os
import webapp2
import jinja2
import urllib2

from google.appengine.ext import db
from webapp2_extras import sessions

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""

config = {} 
config['webapp2_extras.sessions'] = dict(secret_key='')

class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)

    def to_session(self):
        return dict(name=self.name, profile_url=self.profile_url, id=self.id, access_token=self.access_token)


class BaseHandler(webapp2.RequestHandler):  
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        if self.session.get("user"):
            # User is logged in
            return self.session.get("user")
        else:
            # Either used just logged in or just saw the first page
            # We'll see here 
            cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            
            if cookie:
                # Okay so user logged in 
                # Now, check to see if existing user
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    # Not an existing user so get user info
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                        id=str(profile["id"]),
                        name=profile["name"],
                        profile_url=profile["link"],
                        access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                # User is now logged in
                self.session["user"] = user.to_session()
                return self.session.get("user")
        return None
 
    def dispatch(self):
        """ This snippet of code is taken from the webapp2 framework documentation.
        See more at http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
        """
        self.session_store = sessions.get_store(request=self.request)   
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        """ This snippet of code is taken from the webapp2 framework documentation.
        See more at http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
        """
        return self.session_store.get_session()

class HomeHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('example.html')
        self.response.out.write(template.render(dict(facebook_app_id=FACEBOOK_APP_ID, current_user=self.current_user)))
    
    def post(self):
        url = self.request.get('url')
        file = urllib2.urlopen(url)
        graph = facebook.GraphAPI(self.current_user['access_token'])
        response = graph.put_photo(file, "Test Image")
        photo = "http://www.facebook.com/photo.php?fbid={0}".format(response['id'])
        self.redirect(str(photo))

class LogoutHandler(BaseHandler):
    def get(self):
        """ Logout user by setting to None its value in the session"""
        if self.session.get("user") is not None:
            self.session["user"] = None

        self.redirect("/")


app = webapp2.WSGIApplication([('/', HomeHandler), ('/logout', LogoutHandler)], debug=True, config=config)
