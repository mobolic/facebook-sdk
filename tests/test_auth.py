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
# under the License.
import urllib
import facebook
import unittest
from tests.test_facebook import FacebookTestCase


class TestAuthUrl(FacebookTestCase):
    """
    Test that a constructed auth URL matches what we expect
    """
    def test_get_auth_url(self):
        """
        This test is pretty pointless really considering what it does,
        but coverage is coverage
        """
        mock_url = 'http://test.fb/canvas'
        generated_auth_url = facebook.auth_url(self.app_id, mock_url)
        assert(
            generated_auth_url ==
            'https://www.facebook.com/dialog/oauth?redirect_uri=%s&client_id=%s' % (
                urllib.quote_plus(mock_url),
                self.app_id
            )
        )


if __name__ == '__main__':
    unittest.main()