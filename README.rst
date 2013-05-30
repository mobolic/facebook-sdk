===================
Facebook Python SDK
===================

This client library is designed to support the `Facebook Graph API`_ and the
official `Facebook JavaScript SDK`_, which is the canonical way to implement
Facebook authentication. You can read more about the Graph API by accessing its
`official documentation`_.

.. _Facebook Graph API: https://developers.facebook.com/docs/reference/api/
.. _Facebook JavaScript SDK: https://developers.facebook.com/docs/reference/javascript/
.. _official documentation: https://developers.facebook.com/docs/reference/api/

Basic usage:

::

    graph = facebook.GraphAPI(oauth_access_token)
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")
    graph.put_object("me", "feed", message="I am writing on my wall!")

Photo uploads:

::

    graph = facebook.GraphAPI(oauth_access_token)
    tags = json.dumps([{'x':50, 'y':50, 'tag_uid':12345}, {'x':10, 'y':60, 'tag_text':'a turtle'}])
    graph.put_photo(open('img.jpg'), 'Look at this cool photo!', album_id_or_None, tags=tags)

If you are using the module within a web application with the JavaScript SDK,
you can also use the module to use Facebook for login, parsing the cookie set
by the JavaScript SDK for logged in users. For example, in Google AppEngine,
you could get the profile of the logged in user with:

::

    user = facebook.get_user_from_cookie(self.request.cookies, key, secret)
    if user:
        graph = facebook.GraphAPI(user["access_token"])
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")


You can see a full AppEngine example application in examples/appengine.

Reporting Issues
================

If you have bugs or other issues specifically pertaining to this library, file
them `here`_. Bugs with the Graph API should be filed on `Facebook's
bugtracker`_.

.. _here: https://github.com/pythonforfacebook/facebook-sdk/issues
.. _Facebook's bugtracker: https://developers.facebook.com/bugs/


Support & Discussion
====================

Have a question? Need help? Visit the library's `Google Group`_.

.. _Google Group: https://groups.google.com/group/pythonforfacebook
