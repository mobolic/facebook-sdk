#!/usr/bin/env python
#
# Copyright 2013-2014 Martey Dodoo
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
import facebook
import os
import unittest
import sys


class FacebookTestCase(unittest.TestCase):
    """Sets up application ID and secret from environment."""
    def setUp(self):
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            raise Exception("FACEBOOK_APP_ID and FACEBOOK_SECRET "
                            "must be set as environmental variables.")

    def assert_raises_multi_regex(self, expected_exception, expected_regexp, callable_obj=None, *args, **kwargs):
        if sys.version < '2.7':
            # There is no assertRaisesRegexp method in Python 2.6 unittest, so there is need to check it manually
            self.assertRaises(expected_exception, callable_obj, *args, **kwargs)
            try:
                callable_obj(*args)
            except facebook.GraphAPIError as error:
                self.assertEqual(error.message, expected_regexp)
        elif sys.version < '3':
            return self.assertRaisesRegexp(expected_exception, expected_regexp, callable_obj, *args, **kwargs)
        else:
            return self.assertRaisesRegex(expected_exception, expected_regexp, callable_obj, *args, **kwargs)

class TestGetAppAccessToken(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """
    def test_get_app_access_token(self):
        token = facebook.get_app_access_token(self.app_id, self.secret)
        assert (isinstance(token, str) or isinstance(token, unicode))

    def test_get_deleted_app_access_token(self):
        deleted_app_id = '174236045938435'
        deleted_secret = '0073dce2d95c4a5c2922d1827ea0cca6'
        self.assert_raises_multi_regex(facebook.GraphAPIError,
                                       'Error validating application. Application has been deleted.',
                                       facebook.get_app_access_token,
                                       deleted_app_id, deleted_secret)

class TestAPIVersion(FacebookTestCase):
    """Test if using the correct version of Graph API."""
    def test_no_version(self):
        graph = facebook.GraphAPI()
        self.assertNotEqual(graph.version, None, "Version should not be None.")
        self.assertNotEqual(
            graph.version, "", "Version should not be an empty string.")

    def test_version_1_0(self):
        graph = facebook.GraphAPI(version=1.0)
        self.assertEqual(graph.get_version(), 1.0)

    def test_version_2_0(self):
        graph = facebook.GraphAPI(version=2.0)
        self.assertEqual(graph.get_version(), 2.0)

    def test_version_2_1(self):
        graph = facebook.GraphAPI(version=2.1)
        self.assertEqual(graph.get_version(), 2.1)

    def test_version_2_2(self):
        graph = facebook.GraphAPI(version=2.2)
        self.assertEqual(graph.get_version(), 2.2)

    def test_invalid_version(self):
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version=1.2)

    def test_invalid_format(self):
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="1.a")
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="a.1")
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version=1.23)
        self.assertRaises(facebook.GraphAPIError,
                          facebook.GraphAPI, version="1.23")


class TestFQL(FacebookTestCase):
    def test_fql(self):
        graph = facebook.GraphAPI(access_token=facebook.get_app_access_token(
            self.app_id, self.secret), version=2.0)
        # Ensure that version is below 2.1. Facebook has stated that FQL is
        # not present in this or future versions of the Graph API.
        if graph.get_version() < 2.1:
            # This is a tautology, but we are limited in what information
            # we can retrieve with a proper OAuth access token.
            fql_result = graph.fql(
                "SELECT app_id from application where app_id = %s" %
                self.app_id)
            self.assertEqual(fql_result["data"][0]["app_id"], str(self.app_id))


class TestGraphApi(FacebookTestCase):
    def test_bogus_access_token(self):
        graph = facebook.GraphAPI(access_token='wrong_token')
        self.assert_raises_multi_regex(facebook.GraphAPIError, 'Invalid OAuth access token.', graph.get_object, 'me')

    def test_access_with_expired_access_token(self):
        expired_token = 'AAABrFmeaJjgBAIshbq5ZBqZBICsmveZCZBi6O4w9HSTkFI73VMtmkL9j' \
                        'LuWsZBZC9QMHvJFtSulZAqonZBRIByzGooCZC8DWr0t1M4BL9FARdQwPWPnIqCiFQ'
        graph = facebook.GraphAPI(access_token=expired_token)
        self.assert_raises_multi_regex(facebook.GraphAPIError,
                                       'Error validating access token: The session was '
                                       'invalidated explicitly using an API call.',
                                        graph.get_object, 'me')

    def test_with_only_params(self):
        graph = facebook.GraphAPI()
        jerry = graph.get_object('jerry')
        self.assertTrue(jerry['id'], 'User ID should be public.')
        self.assertTrue(jerry['name'], 'User\'s name should be public.')
        self.assertTrue(jerry['first_name'], 'User\'s first name should be public.')
        self.assertTrue(jerry['last_name'], 'User\'s last name should be public.')
        self.assertTrue(jerry['link'], 'User\'s link should be public.')
        self.assertTrue(jerry['username'], 'User\'s username should be public.')

if __name__ == '__main__':
    unittest.main()
