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

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode


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
        # Since "unicode" does not exist in Python 3, we cannot check
        # the following line with flake8 (hence the noqa comment).
        assert(isinstance(token, str) or isinstance(token, unicode))    # noqa


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


class TestAuthURL(FacebookTestCase):
    def test_auth_url(self):
        perms = ['email', 'birthday']
        redirect_url = 'https://localhost/facebook/callback/'

        expected_url = 'https://www.facebook.com/dialog/oauth?' + urlencode(
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


if __name__ == '__main__':
    unittest.main()
