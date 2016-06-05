=============
Tutorials
=============

This page contains tutorials that cover a few of the common use cases when using facebook-sdk.

Authentication
=======================

There are multiple ways to gain an access token in order to use the Graph API. `Check out
their docs`_ to understand the vaious types.

.. _Check out their docs: https://developers.facebook.com/docs/facebook-login/access-tokens

App Access Token
----------------

To gain an App Access Token, you'll need your Facebook App's ``App ID``, ``App Secret``, and ``API Version``. Once
you have them, you can generate an access token through the Graph API's instance method
``get_app_access_token``.

.. code-block:: python

    import facebook

    graph = facebook.GraphAPI(version=2.5)
    graph.access_token = graph.get_app_access_token(
        'your_app_id', 'your_app_secret')
