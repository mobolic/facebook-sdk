#!/usr/bin/env python
#
# Copyright 2010 Facebook
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

"""A Facebook stream client written against the Facebook Graph API."""

FACEBOOK_APP_ID = "your app id"
FACEBOOK_APP_SECRET = "your app secret"

import datetime
import facebook
import os
import os.path
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)


class BaseHandler(webapp.RequestHandler):
    """Provides access to the active Facebook user in self.current_user

    The property is lazy-loaded on first access, using the cookie saved
    by the Facebook JavaScript SDK to determine the user ID of the active
    user. See http://developers.facebook.com/docs/authentication/ for
    more information.
    """
    @property
    def current_user(self):
        """Returns the active user, or None if the user has not logged in."""
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user

    @property
    def graph(self):
        """Returns a Graph API client for the current user."""
        if not hasattr(self, "_graph"):
            if self.current_user:
                self._graph = facebook.GraphAPI(self.current_user.access_token)
            else:
                self._graph = facebook.GraphAPI()
        return self._graph

    def render(self, path, **kwargs):
        args = dict(current_user=self.current_user,
                    facebook_app_id=FACEBOOK_APP_ID)
        args.update(kwargs)
        path = os.path.join(os.path.dirname(__file__), "templates", path)
        self.response.out.write(template.render(path, args))


class HomeHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render("index.html")
            return
        try:
            news_feed = self.graph.get_connections("me", "home")
        except facebook.GraphAPIError:
            self.render("index.html")
            return
        except:
            news_feed = {"data": []}
        for post in news_feed["data"]:
            post["created_time"] = datetime.datetime.strptime(
                post["created_time"], "%Y-%m-%dT%H:%M:%S+0000") + \
                datetime.timedelta(hours=7)
        self.render("home.html", news_feed=news_feed)


class PostHandler(BaseHandler):
    def post(self):
        message = self.request.get("message")
        if not self.current_user or not message:
            self.redirect("/")
            return
        try:
            self.graph.put_wall_post(message)
        except:
            pass
        self.redirect("/")


def main():
    debug = os.environ.get("SERVER_SOFTWARE", "").startswith("Development/")
    util.run_wsgi_app(webapp.WSGIApplication([
        (r"/", HomeHandler),
        (r"/post", PostHandler),
    ], debug=debug))


if __name__ == "__main__":
    main()
