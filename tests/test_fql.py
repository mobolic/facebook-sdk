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
import unittest
from tests.test_facebook import FacebookTestCase


class TestFql(FacebookTestCase):
    """
    Test that a series of FQL queries work as we expect
    """
    def test_get_affliations(self):
        """
        Test to see if we can get affiliations from the Graph API

        Doesn't validate the result, just checks that we get one
        @todo This is just a stub and needs some serious improvement
        """
        api_client = self.get_graph_client()

        result = api_client.fql('SELECT affiliations FROM user WHERE uid = me()')
        assert(type(result) is dict and 'error_code' not in result)


if __name__ == '__main__':
    unittest.main()