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
* ``timeout`` - A ``float`` describing (in seconds) how long the client will
  waiting for a response from Facebook's servers. `See more here`_.
* ``version`` - A ``string`` describing the `version of Facebook's Graph API to
  use`_. Valid API versions are ``1.0``, ``2.0``, ``2.1`` and ``2.2``. The
  default version is ``1.0`` and is used if the version keyword argument is not
  provided.

.. _Read more about access tokens here: https://developers.facebook.com/docs/facebook-login/access-tokens
.. _See more here: http://docs.python-requests.org/en/latest/user/quickstart/#timeouts
.. _version of Facebook's Graph API to use: https://developers.facebook.com/docs/apps/versions

**Example**

.. code-block:: python

    import facebook

    graph = facebook.GraphAPI(access_token='your_token', version='2.2')

Methods
-------

get_object(id, \*\*args)
^^^^^^^^^^^^^^^^^^^^^^^^

Returns the given object from the graph as a ``dict``. A list of
`supported objects can be found here`_.

.. _supported objects can be found here: https://developers.facebook.com/docs/graph-api/reference/

**Parameters**

* ``id`` –  A ``string`` that is a unique ID for that particular resource.

**Example**

.. code-block:: python

    post = graph.get_object(id='post_id')
    print post['message']


get_objects(id, \*\*args)
^^^^^^^^^^^^^^^^^^^^^^^^^

Returns all of the given objects from the graph as a ``dict``. Each given ID
maps to an object.

**Parameters**

* ``ids`` – A ``list`` containing IDs for multiple resources.

**Example**

.. code-block:: python

    post_ids = ['post_id_1', 'post_id_2']
    posts = graph.get_objects(ids=post_ids)

    # Each given id maps to an object.
    for post_id in post_ids:
        print posts[post_id]['created_time']


get_connections(id, connection_name, \*\*args)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns all connections for a given object as a ``dict``.

**Parameters**

* ``id`` – A ``string`` that is a unique ID for that particular resource.
* ``connection_name`` - A ``string`` that specifies the connection or edge
  between objects, e.g., feed, friends, groups, likes, posts. If left empty,
  ``get_connections`` will simply return the authenticated user's basic
  information.

**Example**

.. code-block:: python

    # Get all of the authenticated user's friends
    friends = graph.get_connections(id='me', connection_name='friends')

    # Get all the comments from a post
    comments = graph.get_connections(id='post_id', connection_name='comments')


put_object(parent_object, connection_name, \*\*data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Writes the given object to the graph, connected to the given parent.

**Parameters**

* ``parent_object`` – A ``string`` that is a unique ID for that particular
  resource. The ``parent_object`` is the parent of a connection or edge. E.g.,
  profile is the parent of a feed, and a post is the parent of a comment.
* ``connection_name`` - A ``string`` that specifies the connection or edge
  between objects, e.g., feed, friends, groups, likes, posts.

**Example**

.. code-block:: python

    # Writes 'Hello, world' to the active user's wall.
    graph.put_object(parent_object='me', connection_name='feed',
                     message='Hello, world')

    # Writes a comment on a post
    graph.put_object(parent_object='post_id', connection_name='comments',
                     message='First!')


put_wall_post(message, attachment, profile_id)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Writes a wall post to the given profile's wall. It defaults to writing to the
authenticated user's wall if no ``profile_id`` is specified.

**Parameters**

* ``message`` - A ``string`` that will be posted to the user's wall.
* ``attachment`` - A ``dict`` that adds a structured attachment to the message
  being posted to the Wall. If you are sharing a URL, you will want to use the
  ``attachment`` parameter so that a thumbnail preview appears in the post. It
  should be a ``dict`` of the form:

.. code-block:: python

    attachment =  {
        'name': ''
        'link': '',
        'caption': '',
        'description': '',
        'picture': ''
   }

* ``profile_id`` - A ``string`` that is a unique ID for that particular user.
  Defaults to the authenticated user's wall.

**Example**

.. code-block:: python

    attachment =  {
        'name': 'Link name'
        'link': 'http://www.example.com/',
        'caption': 'Check out this example',
        'description': 'This is a longer description of the attachment',
        'picture': 'http://www.example.com/thumbnail.jpg'
    }

    graph.put_wall_post(message='Check this out...', attachment=attachment)


put_comment(object_id, message)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Writes the given message as a comment on an object.

**Parameters**

* ``object_id`` - A ``string`` that is a unique id for a particular resource.
* ``message`` - A ``string`` that will be posted as the comment.

**Example**

.. code-block:: python

    graph.put_comment(object_id='post_id', message='Great post...')


put_like(object_id)
^^^^^^^^^^^^^^^^^^^

Writes a like to the given object.

**Parameters**

* ``object_id`` - A ``string`` that is a unique id for a particular resource.

**Example**

.. code-block:: python

    graph.put_like(object_id='comment_id')


put_photo(image, message, album_id, \*\*kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Uploads an image using multipart/form-data.

**Parameters**

* ``image`` -  An image of the ``file`` type
* ``message`` - A ``string`` that will caption the image
* ``album_id`` - A ``string`` that is a unique id for an album. If no
  ``album_id`` is provided, the photo posts to /me/photos which uses, or
  creates and uses, an album for your application.

**Example**

.. code-block:: python

    tags = json.dumps([
        {'x':50, 'y':50, 'tag_uid':12345},
        {'x':10, 'y':60, 'tag_text':'a turtle'}
    ])
    graph.put_photo(image=open('img.jpg'), message='Look at this cool photo!',
                    tags=tags)

delete_object(id)
^^^^^^^^^^^^^^^^^

Deletes the object with the given ID from the graph.

**Parameters**

* ``id`` - A ``string`` that is a unique ID for a particular resource.

**Example**

.. code-block:: python

    graph.delete_object(id='post_id')
