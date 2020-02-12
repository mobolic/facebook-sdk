from unittest import mock

import facebook
from . import FacebookTestCase


class FacebookAppSecretProofTestCase(FacebookTestCase):
    """Tests related to application secret proofs."""

    PROOF = "4dad02ff1693df832f9c183fe400fc4f601360be06514acb4a73edb783eec345"

    ACCESS_TOKEN = "abc123"
    APP_SECRET = "xyz789"

    def test_appsecret_proof_set(self):
        """
        Verify that application secret proof is set when a GraphAPI object is
        initialized with an application secret and access token.
        """
        api = facebook.GraphAPI(
            access_token=self.ACCESS_TOKEN, app_secret=self.APP_SECRET
        )
        self.assertEqual(api.app_secret_hmac, self.PROOF)

    def test_appsecret_proof_no_access_token(self):
        """
        Verify that no application secret proof is set when
        a GraphAPI object is initialized with an application secret
        and no access token.
        """
        api = facebook.GraphAPI(app_secret=self.APP_SECRET)
        self.assertEqual(api.app_secret_hmac, None)

    def test_appsecret_proof_no_app_secret(self):
        """
        Verify that no application secret proof is set when
        a GraphAPI object is initialized with no application secret
        and no access token.
        """
        api = facebook.GraphAPI(access_token=self.ACCESS_TOKEN)
        self.assertEqual(api.app_secret_hmac, None)

    @mock.patch("requests.request")
    def test_appsecret_proof_is_set_on_get_request(self, mock_request):
        """
        Verify that no application secret proof is sent with
        GET requests whena GraphAPI object is initialized
        with an application secret and an access token.
        """
        api = facebook.GraphAPI(
            access_token=self.ACCESS_TOKEN, app_secret=self.APP_SECRET
        )
        mock_response = mock.Mock()
        mock_response.headers = {"content-type": "json"}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request("some-path")
        mock_request.assert_called_once_with(
            "GET",
            "https://graph.facebook.com/some-path",
            data=None,
            files=None,
            params={"access_token": "abc123", "appsecret_proof": self.PROOF},
            proxies=None,
            timeout=None,
        )

    @mock.patch("requests.request")
    def test_appsecret_proof_is_set_on_post_request(self, mock_request):
        """
        Verify that no application secret proof is sent with
        POST requests when a GraphAPI object is initialized
        with an application secret and an access token.
        """
        api = facebook.GraphAPI(
            access_token=self.ACCESS_TOKEN, app_secret=self.APP_SECRET
        )
        mock_response = mock.Mock()
        mock_response.headers = {"content-type": "json"}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request("some-path", method="POST")
        mock_request.assert_called_once_with(
            "POST",
            "https://graph.facebook.com/some-path",
            data=None,
            files=None,
            params={"access_token": "abc123", "appsecret_proof": self.PROOF},
            proxies=None,
            timeout=None,
        )

    @mock.patch("requests.request")
    def test_missing_appsecret_proof_is_not_set_on_request(self, mock_request):
        """
        Verify that no application secret proof is set if GraphAPI
        object is initialized without an application secret.
        """
        api = facebook.GraphAPI(access_token=self.ACCESS_TOKEN)
        mock_response = mock.Mock()
        mock_response.headers = {"content-type": "json"}
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response
        api.session.request = mock_request
        api.request("some-path")
        mock_request.assert_called_once_with(
            "GET",
            "https://graph.facebook.com/some-path",
            data=None,
            files=None,
            params={"access_token": "abc123"},
            proxies=None,
            timeout=None,
        )
