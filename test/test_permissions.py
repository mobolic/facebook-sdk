import facebook
from . import FacebookTestCase


class FacebookUserPermissionsTestCase(FacebookTestCase):
    """
    Test if user permissions are retrieved correctly.

    Note that this only tests if the returned JSON object exists and is
    structured as expected, not whether any specific scope is included
    (other than the default `public_profile` scope).

    """

    def test_get_user_permissions_node(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, True
        )
        graph = facebook.GraphAPI(access_token=token)
        self.create_test_users(self.app_id, graph, 1)
        # どのバージョンからかは不明だが、ユーザーデータの中にはアプリのアクセストークンではなく、
        # ユーザーのアクセストークンを使用する必要があることになっている。
        # REF: https://developers.facebook.com/docs/facebook-login/guides/access-tokens#limitations
        user_token = self.test_users[0]["access_token"]
        user_graph = facebook.GraphAPI(access_token=user_token)
        permissions = user_graph.get_permissions(self.test_users[0]["id"])
        self.assertIsNotNone(permissions)
        self.assertTrue("public_profile" in permissions)
        self.assertTrue("user_friends" in permissions)
        self.assertFalse("email" in permissions)

    def test_get_user_permissions_nonexistant_user(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, True
        )
        with self.assertRaises(facebook.GraphAPIError):
            facebook.GraphAPI(token).get_permissions(1)
