import random
import string
import unittest

from facebook import GraphAPIError


class FacebookTestCase(unittest.TestCase):
    """Automated test cases specifically relating to GraphAPIError object."""

    def test_default_error_subcode(self):
        """Verify that default error subcode is None."""
        error = GraphAPIError(None)
        self.assertEqual(error.error_subcode, None)

    def test_setting_error_subcode(self):
        """Verify that error subcode is set properly."""
        # Generate random string.
        error_subcode = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(10)
        )
        result = {
            "error": {
                "message": "",
                "code": "",
                "error_subcode": error_subcode,
            }
        }
        error = GraphAPIError(result)
        self.assertEqual(error.error_subcode, error_subcode)
