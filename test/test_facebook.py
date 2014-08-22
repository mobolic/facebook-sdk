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


class FacebookTestCase(unittest.TestCase):
    """Sets up application ID and secret from environment."""
    def setUp(self):
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            raise Exception("FACEBOOK_APP_ID and FACEBOOK_SECRET "
                            "must be set as environmental variables.")


class TestGetAppAccessToken(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """
    def test_get_app_access_token(self):
        token = facebook.get_app_access_token(self.app_id, self.secret)
        assert(isinstance(token, str) or isinstance(token, unicode))


class TestAPIVersion(FacebookTestCase):
    """Test if using the correct version of Graph API."""
    def test_version_1_0(self):
        graph = facebook.GraphAPI(version=1.0)
        self.assertEqual(graph.get_version(), 1.0)

    def test_version_2_0(self):
        graph = facebook.GraphAPI(version=2.0)
        self.assertEqual(graph.get_version(), 2.0)

    def test_version_2_1(self):
        graph = facebook.GraphAPI(version=2.1)
        self.assertEqual(graph.get_version(), 2.1)

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

if __name__ == '__main__':
    unittest.main()
