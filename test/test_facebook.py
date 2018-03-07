#!/usr/bin/env python
#
# Copyright 2015 Mobolic
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import facebook
import os
import unittest
import inspect

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode

try:
    from unittest import mock
except ImportError:
    import mock


class FacebookTestCase(unittest.TestCase):
    """
    Sets up application ID and secret from environment and initialises an
    empty list for test users.

    """
    def setUp(self):
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            raise Exception("FACEBOOK_APP_ID and FACEBOOK_SECRET "
                            "must be set as environmental variables.")

        self.test_users = []

    def tearDown(self):
        """Deletes the test users included in the test user list."""
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        graph = facebook.GraphAPI(token)

        for user in self.test_users:
            graph.request(user['id'], {}, None, method='DELETE')
        del self.test_users[:]

    def assert_raises_multi_regex(
            self, expected_exception, expected_regexp, callable_obj=None,
            *args, **kwargs):
        """
        Custom function to backport assertRaisesRegexp to all supported
        versions of Python.

        """
        self.assertRaises(expected_exception, callable_obj, *args, **kwargs)
        try:
            callable_obj(*args)
        except facebook.GraphAPIError as error:
            self.assertEqual(error.message, expected_regexp)

    def create_test_users(self, app_id, graph, amount):
        """Function for creating test users."""
        for i in range(amount):
            u = graph.request(app_id + '/accounts/test-users', {}, {},
                              method='POST')
            self.test_users.append(u)

    def create_friend_connections(self, user, friends):
        """Function for creating friend connections for a test user."""
        user_graph = facebook.GraphAPI(user['access_token'])

        for friend in friends:
            if user['id'] == friend['id']:
                continue
            user_graph.request(user['id'] + '/friends/' + friend['id'],
                               {}, {}, method='POST')
            respondent_graph = facebook.GraphAPI(friend['access_token'])
            respondent_graph.request(friend['id'] + '/friends/' + user['id'],
                                     {}, {}, method='POST')


class TestGetAppAccessToken(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """
    def test_get_app_access_token(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        # Since "unicode" does not exist in Python 3, we cannot check
        # the following line with flake8 (hence the noqa comment).
        assert(isinstance(token, str) or isinstance(token, unicode))    # noqa

    def test_get_offline_app_access_token(self):
        """Verify that offline generation of app access tokens works."""
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, offline=True)
        self.assertEqual(token, "{0}|{1}".format(self.app_id, self.secret))

    def test_get_deleted_app_access_token(self):
        deleted_app_id = '174236045938435'
        deleted_secret = '0073dce2d95c4a5c2922d1827ea0cca6'
        deleted_error_message = (
            "Error validating application. Application has been deleted.")

        self.assert_raises_multi_regex(
            facebook.GraphAPIError,
            deleted_error_message,
            facebook.GraphAPI().get_app_access_token,
            deleted_app_id,
            deleted_secret)


class TestAPIVersion(FacebookTestCase):
    """Test if using the correct version of Graph API."""
    def test_no_version(self):
        graph = facebook.GraphAPI()
        self.assertNotEqual(graph.version, None, "Version should not be None.")
        self.assertNotEqual(
            graph.version, "", "Version should not be an empty string.")

    def test_valid_versions(self):
        for version in facebook.VALID_API_VERSIONS:
            graph = facebook.GraphAPI(version=version)
            self.assertEqual(str(graph.get_version()), version)

    def test_invalid_version(self):
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version=1.2)

    def test_invalid_format(self):
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="2.a")
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="a.1")
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version=2.23)
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="2.23")


class TestAuthURL(FacebookTestCase):
    def test_auth_url(self):
        perms = ['email', 'birthday']
        redirect_url = 'https://localhost/facebook/callback/'

        expected_url = facebook.FACEBOOK_OAUTH_DIALOG_URL + urlencode(
            dict(client_id=self.app_id,
                 redirect_uri=redirect_url,
                 scope=','.join(perms)))
        actual_url = facebook.auth_url(self.app_id, redirect_url, perms=perms)

        # Since the order of the query string parameters might be
        # different in each URL, we cannot just compare them to each
        # other.
        expected_url_result = urlparse(expected_url)
        actual_url_result = urlparse(actual_url)
        expected_query = parse_qs(expected_url_result.query)
        actual_query = parse_qs(actual_url_result.query)

        self.assertEqual(actual_url_result.scheme, expected_url_result.scheme)
        self.assertEqual(actual_url_result.netloc, expected_url_result.netloc)
        self.assertEqual(actual_url_result.path, expected_url_result.path)
        self.assertEqual(actual_url_result.params, expected_url_result.params)
        self.assertEqual(actual_query, expected_query)


class TestAccessToken(FacebookTestCase):
    def test_extend_access_token(self):
        """
        Test if extend_access_token requests the correct endpoint.

        Note that this only tests whether extend_access_token returns the
        correct error message when called without a proper user-access token.

        """
        try:
            facebook.GraphAPI().extend_access_token(self.app_id, self.secret)
        except facebook.GraphAPIError as e:
            self.assertEqual(
                e.message, "fb_exchange_token parameter not specified")

    def test_bogus_access_token(self):
        graph = facebook.GraphAPI(access_token='wrong_token')
        self.assertRaises(facebook.GraphAPIError, graph.get_object, 'me')

    def test_access_with_expired_access_token(self):
        expired_token = (
            "AAABrFmeaJjgBAIshbq5ZBqZBICsmveZCZBi6O4w9HSTkFI73VMtmkL9jLuWs"
            "ZBZC9QMHvJFtSulZAqonZBRIByzGooCZC8DWr0t1M4BL9FARdQwPWPnIqCiFQ")
        graph = facebook.GraphAPI(access_token=expired_token)
        self.assertRaises(facebook.GraphAPIError, graph.get_object, 'me')


class TestParseSignedRequest(FacebookTestCase):
    cookie = (
        "O0vd27uj4j6RxdIyMH-VhMwQpUkPgg_9665I9yGDecE."
        "eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURjSXQ2YnhZ"
        "M090T3BSRGtpT1k4UDNlOWgwYzZRNFFuMEFFQnVqR1M3ZEV5LXNtbUt5b3pD"
        "dHdhZy1kRmVYNmRUbi12dVBfQVNtek5RbjlkakloZHJIa0VBMHlLMm16T0Ji"
        "RS1memVoNUh0Vk5UbnpQUDV3Z2VmUkF1bjhvTkQ4S3I3aUd2a3A4Q2EzODJL"
        "NWtqcVl1Z19QV1NUREhqMlY3T2NWaE1GQ2wyWkN2MFk5NnlLUDhfSVAtbnNL"
        "b09kcFVLSU5LMks1SGgxUjZfMkdmMUs1OG5uSnd1bENuSVVRSlhSSU83VEd3"
        "WFJWOVlfa1hzS0pmREpUVzNnTWJ1UGNGc3p0Vkx3MHpyV04yQXE3YWVLVFI2"
        "MFNyeVgzMlBWZkhxNjlzYnUwcnJWLUZMZ2NvMUpBVWlYRlNaY2Q5cVF6WSIs"
        "Imlzc3VlZF9hdCI6MTQ0MTUxNTY1OCwidXNlcl9pZCI6IjEwMTAxNDk2NTUz"
        "NDg2NjExIn0")

    def test_parse_signed_request_when_erroneous(self):
        result = facebook.parse_signed_request(
            signed_request='corrupted.payload',
            app_secret=self.secret)
        self.assertFalse(result)

    def test_parse_signed_request_when_correct(self):
        result = facebook.parse_signed_request(
            signed_request=self.cookie,
            app_secret=self.secret)

        self.assertTrue(result)
        self.assertTrue('issued_at' in result)
        self.assertTrue('code' in result)
        self.assertTrue('user_id' in result)
        self.assertTrue('algorithm' in result)


class TestSearchMethod(FacebookTestCase):
    def setUp(self):
        """Create GraphAPI object that can search (i.e. has user token)."""
        super(TestSearchMethod, self).setUp()
        # Create an app access token to create a test user
        # to create a GraphAPI object with a valid user access token.
        app_token = facebook.GraphAPI().get_app_access_token(self.app_id,
                                                             self.secret,
                                                             True)
        self.create_test_users(self.app_id, facebook.GraphAPI(app_token), 1)
        user = self.test_users[0]
        self.graph = facebook.GraphAPI(user["access_token"])

    def test_valid_search_types(self):
        """Verify that search method accepts all valid search types."""
        for search_type in facebook.VALID_SEARCH_TYPES:
            self.graph.search(type=search_type, q="foobar")

    def test_invalid_search_type(self):
        """Verify that search method fails when an invalid type is passed."""
        search_args = {"type": "foo", "q": "bar"}
        self.assertRaises(
            facebook.GraphAPIError, self.graph.search, search_args)


class TestGetAllConnectionsMethod(FacebookTestCase):

    def test_function_with_zero_connections(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        graph = facebook.GraphAPI(token)

        self.create_test_users(self.app_id, graph, 1)
        friends = graph.get_all_connections(self.test_users[0]['id'],
                                            'friends')

        self.assertTrue(inspect.isgenerator(friends))
        self.assertTrue(len(list(friends)) == 0)

    def test_function_returns_correct_connections(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        graph = facebook.GraphAPI(token)

        self.create_test_users(self.app_id, graph, 27)
        self.create_friend_connections(self.test_users[0], self.test_users)

        friends = graph.get_all_connections(self.test_users[0]['id'],
                                            'friends')
        self.assertTrue(inspect.isgenerator(friends))

        friends_list = list(friends)
        self.assertTrue(len(friends_list) == 26)
        for f in friends:
            self.assertTrue(isinstance(f, dict))
            self.assertTrue('name' in f)
            self.assertTrue('id' in f)


class TestAPIRequest(FacebookTestCase):
    def test_request(self):
        """
        Test if request() works using default value of "args"
        """
        FB_OBJECT_ID = "1846089248954071_1870020306560965"
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        graph = facebook.GraphAPI(access_token=token)

        result = graph.request(FB_OBJECT_ID)
        self.assertEqual(result["created_time"], "2016-12-24T05:20:55+0000")

    def test_request_access_tokens_are_unique_to_instances(self):
        """Verify that access tokens are unique to each GraphAPI object."""
        graph1 = facebook.GraphAPI(access_token="foo")
        graph2 = facebook.GraphAPI(access_token="bar")
        # We use `delete_object` so that the access_token will appear
        # in request.__defaults__.
        try:
            graph1.delete_object("baz")
        except facebook.GraphAPIError:
            pass
        try:
            graph2.delete_object("baz")
        except facebook.GraphAPIError:
            pass
        self.assertEqual(graph1.request.__defaults__[0], None)
        self.assertEqual(graph2.request.__defaults__[0], None)


class TestGetUserPermissions(FacebookTestCase):
    """
    Test if user permissions are retrieved correctly.

    Note that this only tests if the returned JSON object exists and is
    structured as expected, not whether any specific scope is included
    (other than the default `public_profile` scope).

    """
    def test_get_user_permissions_node(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        graph = facebook.GraphAPI(access_token=token)
        self.create_test_users(self.app_id, graph, 1)
        permissions = graph.get_permissions(self.test_users[0]['id'])
        self.assertIsNotNone(permissions)
        self.assertTrue('public_profile' in permissions)
        self.assertTrue('user_friends' in permissions)
        self.assertFalse('email' in permissions)

    def test_get_user_permissions_nonexistant_user(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret)
        with self.assertRaises(facebook.GraphAPIError):
            facebook.GraphAPI(token).get_permissions(1)


class TestAppSecretProof(FacebookTestCase):

    proof = '4dad02ff1693df832f9c183fe400fc4f601360be06514acb4a73edb783eec345'  # noqa

    def test_appsecret_proof_set(self):
        api = facebook.GraphAPI(access_token='abc123', app_secret='xyz789')
        self.assertEqual(api.app_secret_hmac, self.proof)

    def test_appsecret_proof_no_access_token(self):
        api = facebook.GraphAPI(app_secret='xyz789')
        self.assertEqual(api.app_secret_hmac, None)

    def test_appsecret_proof_no_app_secret(self):
        api = facebook.GraphAPI(access_token='abc123')
        self.assertEqual(api.app_secret_hmac, None)

    @mock.patch('requests.request')
    def test_appsecret_proof_is_set_on_get_request(self, mock_request):
        api = facebook.GraphAPI(access_token='abc123', app_secret='xyz789')
        mock_response = mock.Mock()
        mock_response.headers = {'content-type': 'json'}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request('some-path')
        mock_request.assert_called_once_with(
            'GET',
            'https://graph.facebook.com/some-path',
            data=None,
            files=None,
            params={'access_token': 'abc123',
                    'appsecret_proof': self.proof},
            proxies=None,
            timeout=None)

    @mock.patch('requests.request')
    def test_appsecret_proof_is_set_on_post_request(self, mock_request):
        api = facebook.GraphAPI(access_token='abc123', app_secret='xyz789')
        mock_response = mock.Mock()
        mock_response.headers = {'content-type': 'json'}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request('some-path', method='POST')
        mock_request.assert_called_once_with(
            'POST',
            'https://graph.facebook.com/some-path',
            data=None,
            files=None,
            params={'access_token': 'abc123',
                    'appsecret_proof': self.proof},
            proxies=None,
            timeout=None)

    @mock.patch('requests.request')
    def test_missing_appsecret_proof_is_not_set_on_request(self, mock_request):
        api = facebook.GraphAPI(access_token='abc123')
        mock_response = mock.Mock()
        mock_response.headers = {'content-type': 'json'}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request('some-path')
        mock_request.assert_called_once_with(
            'GET',
            'https://graph.facebook.com/some-path',
            data=None,
            files=None,
            params={'access_token': 'abc123'},
            proxies=None,
            timeout=None)


if __name__ == '__main__':
    unittest.main()
