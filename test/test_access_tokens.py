import facebook
from . import FacebookTestCase


class FacebookAccessTokenTestCase(FacebookTestCase):
    def test_extend_access_token(self):
        """
        Test if extend_access_token requests the correct endpoint.

        Note that this only tests whether extend_access_token returns the
        correct error message when called without a proper user-access token.

        """
        try:
            facebook.GraphAPI().extend_access_token(self.app_id, self.secret)
        except facebook.GraphAPIError as e:
            self.assertEqual(
                e.message, "fb_exchange_token parameter not specified"
            )

    def test_bogus_access_token(self):
        graph = facebook.GraphAPI(access_token="wrong_token")
        self.assertRaises(facebook.GraphAPIError, graph.get_object, "me")

    def test_access_with_expired_access_token(self):
        expired_token = (
            "AAABrFmeaJjgBAIshbq5ZBqZBICsmveZCZBi6O4w9HSTkFI73VMtmkL9jLuWs"
            "ZBZC9QMHvJFtSulZAqonZBRIByzGooCZC8DWr0t1M4BL9FARdQwPWPnIqCiFQ"
        )
        graph = facebook.GraphAPI(access_token=expired_token)
        self.assertRaises(facebook.GraphAPIError, graph.get_object, "me")

    def test_request_access_tokens_are_unique_to_instances(self):
        """Verify that access tokens are unique to each GraphAPI object."""
        graph1 = facebook.GraphAPI(access_token="foo")
        graph2 = facebook.GraphAPI(access_token="bar")
        # We use `delete_object` so that the access_token will appear
        # in request.__defaults__.
        try:
            graph1.delete_object("baz")
        except facebook.GraphAPIError:
            pass
        try:
            graph2.delete_object("baz")
        except facebook.GraphAPIError:
            pass
        self.assertEqual(graph1.request.__defaults__[0], None)
        self.assertEqual(graph2.request.__defaults__[0], None)


class FacebookAppAccessTokenCase(FacebookTestCase):
    """
    Test if application access token is returned properly.

    Note that this only tests if the returned token is a string, not
    whether it is valid.

    """

    def test_get_app_access_token(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, False
        )
        # Since "unicode" does not exist in Python 3, we cannot check
        # the following line with flake8 (hence the noqa comment).
        assert isinstance(token, str) or isinstance(token, unicode)  # noqa

    def test_get_offline_app_access_token(self):
        """Verify that offline generation of app access tokens works."""
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, offline=True
        )
        self.assertEqual(token, "{0}|{1}".format(self.app_id, self.secret))

    def test_get_deleted_app_access_token(self):
        deleted_app_id = "174236045938435"
        deleted_secret = "0073dce2d95c4a5c2922d1827ea0cca6"
        deleted_error_message = (
            "Error validating application. Application has been deleted."
        )

        self.assert_raises_multi_regex(
            facebook.GraphAPIError,
            deleted_error_message,
            facebook.GraphAPI().get_app_access_token,
            deleted_app_id,
            deleted_secret,
        )
