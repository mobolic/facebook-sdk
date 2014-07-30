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
   pass

class TestGetAppAccessToken(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """
    def setUp(self):
        """Sets up application ID and secret from environment."""
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            raise Exception("FACEBOOK_APP_ID and FACEBOOK_SECRET "
                            "must be set as environmental variables.")
    def test_get_app_access_token(self):
        token = facebook.get_app_access_token(self.app_id, self.secret)
        self.assertTrue(isinstance(token, str) or isinstance(token, unicode))


class TestGetMe(FacebookTestCase):
    def test_get_me(self):
        access_token = os.environ["FACEBOOK_ACCESS_TOKEN"]
        graph_api = facebook.GraphAPI(access_token)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)

class TestVersioning(FacebookTestCase):
    def test_version_as_number(self):
        access_token = os.environ["FACEBOOK_ACCESS_TOKEN"]
        graph_api = facebook.GraphAPI(access_token, api_version=1)
        self.assertEqual("v1.0/", graph_api.api_version)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)

        graph_api = facebook.GraphAPI(access_token, api_version=2.0)
        self.assertEqual("v2.0/", graph_api.api_version)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)

    def test_version_as_string(self):
        access_token = os.environ["FACEBOOK_ACCESS_TOKEN"]

        graph_api = facebook.GraphAPI(access_token, api_version="1")
        self.assertEqual("v1.0/", graph_api.api_version)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)
        
        graph_api = facebook.GraphAPI(access_token, api_version="v1")
        self.assertEqual("v1.0/", graph_api.api_version)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)

        graph_api = facebook.GraphAPI(access_token, api_version="v2.0")
        self.assertEqual("v2.0/", graph_api.api_version)
        me = graph_api.get_object("me")
        self.assertTrue("name" in me)

if __name__ == '__main__':
    unittest.main()
