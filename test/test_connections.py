import inspect

import facebook
from . import FacebookTestCase


class FacebookAllConnectionsMethodTestCase(FacebookTestCase):
    def test_function_with_zero_connections(self):
        token = facebook.GraphAPI().get_app_access_token(
            self.app_id, self.secret, True
        )
        graph = facebook.GraphAPI(token)

        self.create_test_users(self.app_id, graph, 1)
        friends = graph.get_all_connections(
            self.test_users[0]["id"], "friends"
        )

        self.assertTrue(inspect.isgenerator(friends))
        self.assertTrue(len(list(friends)) == 0)

    # def test_function_returns_correct_connections(self):
    #     token = facebook.GraphAPI().get_app_access_token(
    #         self.app_id, self.secret, True
    #     )
    #     graph = facebook.GraphAPI(token)

    #     self.create_test_users(self.app_id, graph, 3)
    #     self.create_friend_connections(self.test_users[0], self.test_users)

    #     friends = graph.get_all_connections(
    #         self.test_users[0]["id"], "friends"
    #     )
    #     self.assertTrue(inspect.isgenerator(friends))

    #     friends_list = list(friends)
    #     self.assertTrue(len(friends_list) == 2)
    #     for f in friends:
    #         self.assertTrue(isinstance(f, dict))
    #         self.assertTrue("name" in f)
    #         self.assertTrue("id" in f)
