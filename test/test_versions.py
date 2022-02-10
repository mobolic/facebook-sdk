import facebook
from . import FacebookTestCase


class FacebookAPIVersionTestCase(FacebookTestCase):
    """Test if using the correct version of Graph API."""

    def test_no_version(self):
        graph = facebook.GraphAPI()
        self.assertNotEqual(graph.version, None, "Version should not be None.")
        self.assertNotEqual(
            graph.version, "", "Version should not be an empty string."
        )

    def test_valid_versions(self):
        graph = facebook.GraphAPI(version=facebook.DEFAULT_VERSION)
        self.assertEqual(str(graph.get_version()), facebook.DEFAULT_VERSION)

    def test_invalid_version(self):
        self.assertRaises(
            facebook.GraphAPIError, facebook.GraphAPI, version=1.2
        )

    def test_invalid_format(self):
        self.assertRaises(
            facebook.GraphAPIError, facebook.GraphAPI, version="2.a"
        )
        self.assertRaises(
            facebook.GraphAPIError, facebook.GraphAPI, version="a.1"
        )
        self.assertRaises(
            facebook.GraphAPIError, facebook.GraphAPI, version=2.23
        )
        self.assertRaises(
            facebook.GraphAPIError, facebook.GraphAPI, version="2.23"
        )
