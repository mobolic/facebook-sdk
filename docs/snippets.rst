===============
Sample Snippets
===============

Basic usage
===========

The below snippet will return a json with all public profile information for the given facebook id and their friends list.

::

    import facebook
    graph = facebook.GraphAPI(oauth_access_token)
    profile = graph.get_object("me")
    print profile
    friends = graph.get_connections("me", "friends")
    print friends



Filtering fields
================

The below snippet will return a json with id, likes, first_name for the given facebook id.

::

    import facebook
    facebookParams = {'fields' : 'id,likes.limit(1000000),first_name',}
    graph = facebook.GraphAPI(oauth_access_token)
    profile = graph.get_object("me", **facebookParams)
    print profile