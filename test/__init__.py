#!/usr/bin/env python
#
# Copyright 2015-2019 Mobolic
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import unittest

import facebook


class FacebookTestCase(unittest.TestCase):
    """
    Sets up application ID and secret from environment and initialises an
    empty list for test users.

    """

    def setUp(self):
        try:
            self.app_id = os.environ["FACEBOOK_APP_ID"]
            self.secret = os.environ["FACEBOOK_SECRET"]
        except KeyError:
            raise Exception(
                "FACEBOOK_APP_ID and FACEBOOK_SECRET "
                "must be set as environmental variables."
            )

        self.test_users = []

    def tearDown(self):
        """Deletes the test users included in the test user list."""
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, True
        )
        graph = facebook.GraphAPI(token)

        for user in self.test_users:
            graph.request(user["id"], {}, None, method="DELETE")
        del self.test_users[:]

    def assert_raises_multi_regex(
        self,
        expected_exception,
        expected_regexp,
        callable_obj=None,
        *args,
        **kwargs
    ):
        """
        Custom function to backport assertRaisesRegexp to all supported
        versions of Python.

        """
        self.assertRaises(expected_exception, callable_obj, *args, **kwargs)
        try:
            callable_obj(*args)
        except facebook.GraphAPIError as error:
            self.assertEqual(error.message, expected_regexp)

    def create_test_users(self, app_id, graph, amount):
        """Function for creating test users."""
        for i in range(amount):
            u = graph.request(
                app_id + "/accounts/test-users", {}, {}, method="POST"
            )
            self.test_users.append(u)

    def create_friend_connections(self, user, friends):
        """Function for creating friend connections for a test user."""
        user_graph = facebook.GraphAPI(user["access_token"])

        for friend in friends:
            if user["id"] == friend["id"]:
                continue
            user_graph.request(
                user["id"] + "/friends/" + friend["id"], {}, {}, method="POST"
            )
            respondent_graph = facebook.GraphAPI(friend["access_token"])
            respondent_graph.request(
                friend["id"] + "/friends/" + user["id"], {}, {}, method="POST"
            )
