import facebook
from . import FacebookTestCase


class FacebookSearchTestCase(FacebookTestCase):
    def setUp(self):
        """Create GraphAPI object that can search (i.e. has user token)."""
        super(FacebookSearchTestCase, self).setUp()
        # Create an app access token to create a test user
        # to create a GraphAPI object with a valid user access token.
        app_token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, True
        )
        self.create_test_users(self.app_id, facebook.GraphAPI(app_token), 1)
        user = self.test_users[0]
        self.graph = facebook.GraphAPI(user["access_token"])

    # def test_valid_search_types(self):
    #     """Verify that search method accepts all valid search types."""
    #     for search_type in facebook.VALID_SEARCH_TYPES:
    #         self.graph.search(type=search_type, q="foobar")

    def test_invalid_search_type(self):
        """Verify that search method fails when an invalid type is passed."""
        search_args = {"type": "foo", "q": "bar"}
        self.assertRaises(
            facebook.GraphAPIError, self.graph.search, search_args
        )
