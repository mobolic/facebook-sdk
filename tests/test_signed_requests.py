#!/usr/bin/env python
#
# Copyright 2013 Nick Pack
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
# under the License
import base64
import hashlib
import hmac
import json
import unittest
import facebook
from tests.test_facebook import FacebookTestCase


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

    def generate_sr_payload(self, secret):
        """
        Generate a mock signed request

        :param secret: Secret key to sign the request with
        :type secret: str
        :return: Encoded signed request string
        :rtype: str
        """
        encoded_payload = base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD).encode('ascii'))

        signature = hmac.new(
            secret,
            msg=encoded_payload,
            digestmod=hashlib.sha256
        ).digest()

        return "%s.%s" % (
            base64.urlsafe_b64encode(signature),
            base64.urlsafe_b64encode(json.dumps(self.TEST_PAYLOAD))
        )

    def test_valid_signed_request_parse(self):
        """
        Construct a valid signed request token, and run it through the parser
        """
        assert(
            facebook.parse_signed_request(
                self.generate_sr_payload(self.secret),
                self.secret
            ) == self.TEST_PAYLOAD
        )

    def test_invalid_signed_request_parse(self):
        """
        Construct a signed request with an invalid secret, and run it through the parser
        """
        assert(
            not facebook.parse_signed_request(
                self.generate_sr_payload('THISISANONSENSESECRETTOgenerateAfaIlIngToken'),
                self.secret
            )
        )

if __name__ == '__main__':
    unittest.main()
