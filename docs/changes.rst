=========
Changelog
=========

Version 3.0.0 (unreleased)
========================
 - Remove support for Python 2.6.
 - Add support for Graph API version 2.8.
 - Remove support for Graph API version 2.1.
 - Change default Graph API version to 2.2.
 - Add support for requests' sessions (#201).
 - Add versioning to access token endpoints (#322).
 - Add new `get_all_connections` method to make pagination easier (#337).
 - Add new `get_permissions` method to retrieve permissions that a user has
   granted an application (#264, #342).

Version 2.0.0 (2016-08-08)
==============================
 - Add support for Graph API versions 2.6 and 2.7.
 - Remove support for Graph API version 2.0 and FQL.
 - Change default Graph API version to 2.1.
 - Fix bug with debug_access_token method not working when the
   GraphAPI object's access token was set (#276).
 - Allow offline generation of application access tokens.

Version 1.0.0 (2016-04-01)
==========================

 - Python 3 support.
 - More comprehensive test coverage.
 - Full Unicode support.
 - Better exception handling.
 - Vastly improved documentation.

Version 0.4.0 (2012-10-15)
==========================

 - Add support for deleting application requests.
 - Fix minor documentation error in README.
 - Verify signed request parsing succeeded when creating OAuth token.
 - Convert README to ReStructuredText.

Version 0.3.2 (2012-07-28)
==========================

 - Add support for state parameters in auth dialog URLs.
 - Fixes bug with Unicode app secrets.
 - Add optional timeout support for faster API requests.
 - Random PEP8 compliance fixes.

Version 0.3.1 (2012-05-16)
==========================

 - Minor documentation updates.
 - Removes the develop branch in favor of named feature branches.
