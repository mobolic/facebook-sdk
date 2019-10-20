import facebook
from . import FacebookTestCase


class FacebookParseSignedRequestTestCase(FacebookTestCase):
    cookie = (
        "Z6pnNcY-TePEBA7IfKta6ipLgrig53M7DRGisKSybBQ."
        "eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURjSXQ2YnhZ"
        "M090T3BSRGtpT1k4UDNlOWgwYzZRNFFuMEFFQnVqR1M3ZEV5LXNtbUt5b3pD"
        "dHdhZy1kRmVYNmRUbi12dVBfQVNtek5RbjlkakloZHJIa0VBMHlLMm16T0Ji"
        "RS1memVoNUh0Vk5UbnpQUDV3Z2VmUkF1bjhvTkQ4S3I3aUd2a3A4Q2EzODJL"
        "NWtqcVl1Z19QV1NUREhqMlY3T2NWaE1GQ2wyWkN2MFk5NnlLUDhfSVAtbnNL"
        "b09kcFVLSU5LMks1SGgxUjZfMkdmMUs1OG5uSnd1bENuSVVRSlhSSU83VEd3"
        "WFJWOVlfa1hzS0pmREpUVzNnTWJ1UGNGc3p0Vkx3MHpyV04yQXE3YWVLVFI2"
        "MFNyeVgzMlBWZkhxNjlzYnUwcnJWLUZMZ2NvMUpBVWlYRlNaY2Q5cVF6WSIs"
        "Imlzc3VlZF9hdCI6MTQ0MTUxNTY1OCwidXNlcl9pZCI6IjEwMTAxNDk2NTUz"
        "NDg2NjExIn0"
    )

    def test_parse_signed_request_when_erroneous(self):
        result = facebook.parse_signed_request(
            signed_request="corrupted.payload", app_secret=self.secret
        )
        self.assertFalse(result)

    def test_parse_signed_request_when_correct(self):
        result = facebook.parse_signed_request(
            signed_request=self.cookie, app_secret=self.secret
        )

        self.assertTrue(result)
        self.assertTrue("issued_at" in result)
        self.assertTrue("code" in result)
        self.assertTrue("user_id" in result)
        self.assertTrue("algorithm" in result)
