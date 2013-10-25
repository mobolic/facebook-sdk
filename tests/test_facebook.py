#!/usr/bin/env python
#
# Copyright 2013 Martey Dodoo
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
import urllib2

from StringIO import StringIO


class FacebookTestCase(unittest.TestCase):
    """Sets up application ID and secret from environment."""
    def setUp(self):
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            self.skipTest("FACEBOOK_APP_ID and FACEBOOK_SECRET must be set as "
                          "environmental variables.")


class FakeFileInfo(object):
    """
    File info that can be returned with the a call to a stream's info method
    """
    attrs = {
        'maintype': 'text',
        'content-type': 'application/json',
    }

    def __getitem__(self, name):
        return getattr(self, name)

    def __init__(self, attrs=None):
        self.__dict__.update(self.attrs)
        if attrs:
            self.__dict__.update(attrs)


class FakeHTTPError(StringIO, urllib2.HTTPError):
    """
    Mocks out HTTPError with a StringIO so that we can make it look like an
    HTTP stream
    """
    pass


class MockURLOpenTestCase(unittest.TestCase):
    """
    Mocks out URLOpen so that there are no external deps for the test
    """

    urlopen_args = None
    urlopen_kwargs = None
    urlopen_raise = None
    urlopen_return = None

    def fake_file(self, string='{}', url='http://bogus', info=None):
        sio = StringIO(string)
        sio.info = lambda: FakeFileInfo(info)
        sio.url = url
        return sio

    def fake_httperror(self, string='{}'):
        return FakeHTTPError(string)

    def setUp(self):
        self.api = facebook.GraphAPI()
        self.urlopen = urllib2.urlopen

        def urlopen(*args, **kwargs):
            self.urlopen_args = args
            self.urlopen_kwargs = kwargs

            if self.urlopen_raise:
                raise self.urlopen_raise

            return self.urlopen_return

        urllib2.urlopen = urlopen


class TestGetAppAccessToken(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """
    def test_get_app_access_token(self):
        assert(isinstance(facebook.get_app_access_token(
            self.app_id, self.secret), str))


class RawRequestTestCase(MockURLOpenTestCase):
    """
    Sets up application ID and secret from environment.
    """

    def test_simple_json(self):
        """
        Simple JSON return
        """

        self.urlopen_return = self.fake_file("""{
            "message": "here"
        }""")
        self.assertEqual(self.api.raw_request(None), {'message': 'here'})

    def test_image(self):
        """
        Image returned
        """

        self.urlopen_return = self.fake_file('bogus image',
                                             info={'maintype': 'image'})
        self.assertEqual(self.api.raw_request(None),
                         {'data': 'bogus image',
                          'mime-type': 'application/json',
                          'url': 'http://bogus'})

    def test_timeout(self):
        """
        Make sure timout is set as expected.
        """

        self.urlopen_return = self.fake_file()
        self.api.timeout = 33
        self.api.raw_request(None)
        self.assertEqual(self.urlopen_kwargs['timeout'], 33)

    def test_http_error(self):
        """
        GraphAPIError should be raised to wrap HTTPError
        """

        self.urlopen_raise = self.fake_httperror()
        self.assertRaises(facebook.GraphAPIError, self.api.raw_request, [None])

    def test_bad_maintype(self):
        """
        Return with unknown maintype
        """

        self.urlopen_return = self.fake_file('{}', info={'maintype': 'bogus'})
        self.assertRaises(facebook.GraphAPIError, self.api.raw_request, [None])

    def test_other_error(self):
        """
        GraphAPIError should be raised when there's error data in the JSON
        """

        self.urlopen_return = self.fake_file("""{
            "error": {
                "type": "a thing",
                "message": "move along"
            }
        }""")
        self.assertRaises(facebook.GraphAPIError, self.api.raw_request, [None])


if __name__ == '__main__':
    unittest.main()
