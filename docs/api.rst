=====================
API Reference
=====================

This page contains specific information on the SDK's classes, methods and functions.

class facebook.GraphAPI
========
A client for the Facebook Graph API. The Graph API is made up of the objects or
nodes in Facebook (e.g., people, pages, events, photos) and the connections or
edges between them (e.g., friends, photo tags, and event RSVPs). This client
provides access to those primitive types in a generic way.

You can read more about `Facebook's Graph API here`_.

.. _Facebook's Graph API here: https://developers.facebook.com/docs/graph-api

**Parameters**

* *access_token (optional)* – A string that identifies a user, app, or page and can be used by the app to make graph API calls. `Read more about access tokens here`_.
* *timeout (optional)* - A float describing the timeout of the request in seconds. I.e., you can tell the client to stop waiting for a response after a given number of seconds with the timeout parameter. `See more here`_.
* *version (optional)* - TODO

.. _Read more about access tokens here: https://developers.facebook.com/docs/facebook-login/access-tokens
.. _See more here: http://docs.python-requests.org/en/latest/user/quickstart/#timeouts

**Example**

.. code-block:: python

   import facebook

   graph = facebook.GraphAPI(access_token='your_token')
