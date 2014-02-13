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
    access_token = os.environ["FACEBOOK_ACCESS_TOKEN"]
except KeyError:
    raise Exception("FACEBOOK_ACCESS_TOKEN must be set as an environment "
                    "variable.")


class FacebookTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = facebook.GraphAPI(access_token)


class SimpleTests(FacebookTestCase):
    # TODO: write more tests to try basic functionality!
    def test_get_object(self):
        result = self.graph.get_object("me")
        self.assertTrue('id' in result)


class BatchTests(FacebookTestCase):
    def test_batch_request(self):
        self.assertFalse(self.graph._batch_request)
        with self.graph as batch:
            self.assertTrue(batch._batch_request)
            self.assertTrue(self.graph._batch_request)
            # Test a couple of good requests
            batch.get_object("me")
            batch.get_connections("me", "friends")
            # And one bad one
            batch.get_connections("me", "foo")
        self.assertFalse(self.graph._batch_request)
        results = self.graph.execute()
        self.assertEqual(len(results), 3)
        me_result, friends_result, bad_result = results
        self.assertTrue('id' in me_result)
        self.assertTrue('data' in friends_result)
        # Assume everyone has at least one friend!
        self.assertGreater(len(friends_result['data']), 0)
        self.assertTrue(isinstance(bad_result, facebook.GraphAPIError))


if __name__ == '__main__':
    unittest.main()
