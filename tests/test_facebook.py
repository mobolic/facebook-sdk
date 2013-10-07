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
import os
import unittest
import facebook


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

    def get_graph_client(self):
        """
        Get an instance of the Graph API client
        """
        return facebook.GraphAPI(
            facebook.get_app_access_token(self.app_id, self.secret)
        )