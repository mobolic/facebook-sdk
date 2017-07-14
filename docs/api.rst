=============
API Reference
=============

This page contains specific information on the SDK's classes, methods and
functions.

class facebook.GraphAPI
=======================

A client for the Facebook Graph API. The Graph API is made up of the objects or
nodes in Facebook (e.g., people, pages, events, photos) and the connections or
edges between them (e.g., friends, photo tags, and event RSVPs). This client
provides access to those primitive types in a generic way.

You can read more about `Facebook's Graph API here`_.

.. _Facebook's Graph API here: https://developers.facebook.com/docs/graph-api

**Parameters**

* ``access_token`` – A ``string`` that identifies a user, app, or page and can
  be used by the app to make graph API calls.
  `Read more about access tokens here`_.
* ``timeout`` - A ``float`` describing (in seconds) how long the client will be
  waiting for a response from Facebook's servers. `See more here`_.
* ``version`` - A ``string`` describing the `version of Facebook's Graph API to
  use`_. The default version is the oldest current version. It is used if
  the version keyword argument is not provided.
* ``proxies`` - A ``dict`` with proxy-settings that Requests should use.
  `See Requests documentation`_.
* ``session`` - A `Requests Session object`_.

.. _Read more about access tokens here: https://developers.facebook.com/docs/facebook-login/access-tokens
.. _See more here: http://docs.python-requests.org/en/latest/user/quickstart/#timeouts
.. _version of Facebook's Graph API to use: https://developers.facebook.com/docs/apps/changelog#versions
.. _See Requests documentation: http://www.python-requests.org/en/latest/user/advanced/#proxies
.. _Requests Session object: http://docs.python-requests.org/en/master/user/advanced/#session-objects

**Example**

.. code-block:: python

    import facebook

    graph = facebook.GraphAPI(access_token="your_token", version="2.12")

Methods
-------

get_object
^^^^^^^^^^

Returns the given object from the graph as a ``dict``. A list of
`supported objects can be found here`_.

.. _supported objects can be found here: https://developers.facebook.com/docs/graph-api/reference/

**Parameters**

* ``id`` –  A ``string`` that is a unique ID for that particular resource.
* ``**args`` (optional) - keyword args to be passed as query params

**Examples**

.. code-block:: python

    # Get the message from a post.
    post = graph.get_object(id='post_id', fields='message')
    print(post['message'])

.. code-block:: python

    # Retrieve the number of people who say that they are attending or
    # declining  to attend a specific event.
    event = graph.get_object(id='event_id',
                             fields='attending_count,declined_count')
    print(event['attending_count'])
    print(event['declined_count'])

.. code-block:: python

    # Retrieve information about a website or page:
    # https://developers.facebook.com/docs/graph-api/reference/url/
    # Note that URLs need to be properly encoded with the "quote" function
    # of urllib (Python 2) or urllib.parse (Python 3).
    site_info = graph.get_object(id="https%3A//mobolic.com",
                                 fields="og_object")
    print(site_info["og_object"]["description"])

get_objects
^^^^^^^^^^^

Returns all of the given objects from the graph as a ``dict``. Each given ID
maps to an object.

**Parameters**

* ``ids`` – A ``list`` containing IDs for multiple resources.
* ``**args`` (optional) - keyword args to be passed as query params

**Examples**

.. code-block:: python

    # Get the time two different posts were created.
    post_ids = ['post_id_1', 'post_id_2']
    posts = graph.get_objects(ids=post_ids, fields="created_time")

    for post in posts:
        print(post['created_time'])

.. code-block:: python

    # Get the number of people attending or who have declined to attend
    # two different events.
    event_ids = ['event_id_1', 'event_id_2']
    events = graph.get_objects(ids=event_ids, fields='attending_count,declined_count')

    for event in events:
        print(event['declined_count'])

search
^^^^^^

https://developers.facebook.com/docs/places/search

Valid types are: place, placetopic

**Parameters**

* ``type`` – A ``string`` containing a valid type.
* ``**args`` (optional) - keyword args to be passed as query params

**Example**

.. code-block:: python

    # Search for places near 1 Hacker Way in Menlo Park, California.
    places = graph.search(type='place',
                          center='37.4845306,-122.1498183',
                          fields='name,location')

    # Each given id maps to an object the contains the requested fields.
    for place in places['data']:
        print('%s %s' % (place['name'].encode(),place['location'].get('zip')))

get_connections
^^^^^^^^^^^^^^^

Returns all connections for a given object as a ``dict``.

**Parameters**

* ``id`` – A ``string`` that is a unique ID for that particular resource.
* ``connection_name`` - A ``string`` that specifies the connection or edge
  between objects, e.g., feed, friends, groups, likes, posts. If left empty,
  ``get_connections`` will simply return the authenticated user's basic
  information.

**Examples**

.. code-block:: python

    # Get the active user's friends.
    friends = graph.get_connections(id='me', connection_name='friends')

    # Get the comments from a post.
    comments = graph.get_connections(id='post_id', connection_name='comments')


get_all_connections
^^^^^^^^^^^^^^^^^^^

Iterates over all pages returned by a get_connections call and yields the
individual items.

**Parameters**

* ``id`` – A ``string`` that is a unique ID for that particular resource.
* ``connection_name`` - A ``string`` that specifies the connection or edge
  between objects, e.g., feed, friends, groups, likes, posts.

put_object
^^^^^^^^^^

Writes the given object to the graph, connected to the given parent.

**Parameters**

* ``parent_object`` – A ``string`` that is a unique ID for that particular
  resource. The ``parent_object`` is the parent of a connection or edge. E.g.,
  profile is the parent of a feed, and a post is the parent of a comment.
* ``connection_name`` - A ``string`` that specifies the connection or edge
  between objects, e.g., feed, friends, groups, likes, posts.

**Examples**

.. code-block:: python

    # Write 'Hello, world' to the active user's wall.
    graph.put_object(parent_object='me', connection_name='feed',
                     message='Hello, world')

   # Add a link and write a message about it.
   graph.put_object(
      parent_object="me",
      connection_name="feed",
      message="This is a great website. Everyone should visit it.",
      link="https://www.facebook.com")

    # Write a comment on a post.
    graph.put_object(parent_object='post_id', connection_name='comments',
                     message='First!')

put_comment
^^^^^^^^^^^

Writes the given message as a comment on an object.

**Parameters**

* ``object_id`` - A ``string`` that is a unique id for a particular resource.
* ``message`` - A ``string`` that will be posted as the comment.

**Example**

.. code-block:: python

    graph.put_comment(object_id='post_id', message='Great post...')


put_like
^^^^^^^^

Writes a like to the given object.

**Parameters**

* ``object_id`` - A ``string`` that is a unique id for a particular resource.

**Example**

.. code-block:: python

    graph.put_like(object_id='comment_id')


put_photo
^^^^^^^^^

https://developers.facebook.com/docs/graph-api/reference/user/photos#publish

Upload an image using multipart/form-data. Returns JSON with the IDs of the
photo and its post.

**Parameters**

  * ``image`` - A file object representing the image to be uploaded.
  * ``album_path`` - A path representing where the image should be uploaded.
    Defaults to `/me/photos` which creates/uses a custom album for each
    Facebook application.

**Examples**

.. code-block:: python

    # Upload an image with a caption.
    graph.put_photo(image=open('img.jpg', 'rb'),
                    message='Look at this cool photo!')

    # Upload a photo to an album.
    graph.put_photo(image=open("img.jpg", 'rb'),
                    album_path=album_id + "/photos")

    # Upload a profile photo for a Page.
    graph.put_photo(image=open("img.jpg", 'rb'),
                    album_path=page_id + "/picture")

delete_object
^^^^^^^^^^^^^

Deletes the object with the given ID from the graph.

**Parameters**

* ``id`` - A ``string`` that is a unique ID for a particular resource.

**Example**

.. code-block:: python

    graph.delete_object(id='post_id')

get_permissions
^^^^^^^^^^^^^^^

https://developers.facebook.com/docs/graph-api/reference/user/permissions/

Returns the permissions granted to the app by the user with the given ID as a
``set``.

**Parameters**

* ``user_id`` - A ``string`` containing a user's unique ID.

**Example**

.. code-block:: python

    # Figure out whether the specified user has granted us the
    # "public_profile" permission.
    permissions = graph.get_permissions(user_id=12345)
    print('public_profile' in permissions)

get_auth_url
^^^^^^^^^^^^

https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow

Returns a Facebook login URL used to request an access token and permissions.

**Parameters**

* ``app_id`` - A ``string`` containing a Facebook appplication ID.
* ``canvas_url`` - A ``string`` containing the URL where Facebook should
  redirect after successful authentication.
* ``perms`` - An optional ``list`` of requested Facebook permissions.

**Example**

.. code-block:: python

    app_id = "1231241241"
    canvas_url = "https://domain.com/that-handles-auth-response/"
    perms = ["manage_pages","publish_pages"]
    fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
    print(fb_login_url)
