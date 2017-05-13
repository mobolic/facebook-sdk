#!/usr/bin/env python
#
# Copyright 2010 Facebook
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

"""A barebones Tornado application that uses Facebook for login.

Assumes a database with a schema as specified in schema.sql. We store a
local copy of basic user data so we don't need to make a round-trip to
the Facebook API on every request once a user has logged in.
"""

import facebook
import tornado.database
import tornado.httpserver
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("facebook_app_id", help="Facebook Application ID")
define("facebook_app_secret", help="Facebook Application Secret")
define("mysql_host", help="MySQL database host")
define("mysql_database", help="MySQL database database")
define("mysql_user", help="MySQL database user")
define("mysql_password", help="MySQL database password")


class BaseHandler(tornado.web.RequestHandler):
    """Implements authentication via the Facebook JavaScript SDK cookie."""
    def get_current_user(self):
        cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
        cookie = facebook.get_user_from_cookie(
            cookies, options.facebook_app_id, options.facebook_app_secret)
        if not cookie:
            return None
        user = self.db.get(
            "SELECT * FROM users WHERE id = %s", cookie["uid"])
        if not user:
            # TODO: Make this fetch async rather than blocking
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me")
            self.db.execute(
                "REPLACE INTO users (id, name, profile_url, access_token) "
                "VALUES (%s,%s,%s,%s)", profile["id"], profile["name"],
                profile["link"], cookie["access_token"])
            user = self.db.get(
                "SELECT * FROM users WHERE id = %s", profile["id"])
        elif user.access_token != cookie["access_token"]:
            self.db.execute(
                "UPDATE users SET access_token = %s WHERE id = %s",
                cookie["access_token"], user.id)
        return user

    @property
    def db(self):
        if not hasattr(BaseHandler, "_db"):
            BaseHandler._db = tornado.database.Connection(
                host=options.mysql_host, database=options.mysql_database,
                user=options.mysql_user, password=options.mysql_password)
        return BaseHandler._db


class MainHandler(BaseHandler):
    def get(self):
        self.render("example.html", options=options)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application([
        (r"/", MainHandler),
    ]))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
