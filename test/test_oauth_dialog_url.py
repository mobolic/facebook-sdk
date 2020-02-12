from urllib.parse import parse_qs, urlencode, urlparse

import facebook
from . import FacebookTestCase


class FacebookAuthURLTestCase(FacebookTestCase):
    def test_auth_url(self):
        graph = facebook.GraphAPI()
        perms = ["email", "birthday"]
        redirect_url = "https://localhost/facebook/callback/"

        encoded_args = urlencode(
            dict(
                client_id=self.app_id,
                redirect_uri=redirect_url,
                scope=",".join(perms),
            )
        )
        expected_url = "{0}{1}/{2}{3}".format(
            facebook.FACEBOOK_WWW_URL,
            graph.version,
            facebook.FACEBOOK_OAUTH_DIALOG_PATH,
            encoded_args,
        )

        actual_url = graph.get_auth_url(self.app_id, redirect_url, perms=perms)

        # Since the order of the query string parameters might be
        # different in each URL, we cannot just compare them to each
        # other.
        expected_url_result = urlparse(expected_url)
        actual_url_result = urlparse(actual_url)
        expected_query = parse_qs(expected_url_result.query)
        actual_query = parse_qs(actual_url_result.query)

        self.assertEqual(actual_url_result.scheme, expected_url_result.scheme)
        self.assertEqual(actual_url_result.netloc, expected_url_result.netloc)
        self.assertEqual(actual_url_result.path, expected_url_result.path)
        self.assertEqual(actual_url_result.params, expected_url_result.params)
        self.assertEqual(actual_query, expected_query)
