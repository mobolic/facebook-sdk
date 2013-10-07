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
import base64
import hashlib
import hmac
import json
import facebook
import os
import unittest


class FacebookTestCase(unittest.TestCase):
    """
    Sets up application ID and secret from environment.
    """
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
        assert(isinstance(facebook.get_app_access_token(
            self.app_id, self.secret), str))


class TestSignedRequestParser(FacebookTestCase):
    """
    Test if the application can parse a valid signed request object
    """
    # Payload borrowed from FB docs
    TEST_PAYLOAD = {
        "oauth_token": "S0meInvEnt3dT0k3n",
        "algorithm": "HMAC-SHA256",
        "expires": 1291840400,
        "issued_at": 1291836800,
        "user_id": "218471"
    }

    def test_valid_signed_request_parse(self):
        """
        Construct a signed request token, and run it through the parser
        """
        encoded_payload = base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD).encode('ascii'))

        signature = hmac.new(
            self.secret,
            msg=encoded_payload,
            digestmod=hashlib.sha256
        ).digest()

        token = "%s.%s" % (
            base64.urlsafe_b64encode(signature),
            base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD))
        )

        assert(facebook.parse_signed_request(token, self.secret) == self.TEST_PAYLOAD)

    def test_invalid_signed_request_parse(self):
        """
        Construct a signed request with an invalid secret, and run it through the parser
        """
        encoded_payload = base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD).encode('ascii'))

        signature = hmac.new(
            'THISISANONSENSESECRETTOgenerateAfaIlIngToken',
            msg=encoded_payload,
            digestmod=hashlib.sha256
        ).digest()

        token = "%s.%s" % (
            base64.urlsafe_b64encode(signature),
            base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD))
        )

        assert(not facebook.parse_signed_request(token, self.secret))

if __name__ == '__main__':
    unittest.main()
