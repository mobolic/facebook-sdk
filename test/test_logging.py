try:
    from unittest import mock
except ImportError:
    import mock

import logging
import facebook
from . import FacebookTestCase

logger = logging.getLogger(__name__)


class FacebookLoggingTestCase(FacebookTestCase):
    def test_log_request(self):
        with mock.patch("logging.Logger.info") as m:
            facebook.GraphAPILogger(
                logger, facebook.LoggingVerbosity.BASIC_REQUEST_INFO
            ).log_request("GET", "/insights", {"fields": "x,y,z"}, None)
            assert m.call_args_list == [
                mock.call("Request method: GET"),
                mock.call("Request URL: /insights"),
                mock.call("Request Args: {'fields': 'x,y,z'}"),
                mock.call("Request Post Args: None"),
            ]

    def test_log_response(self):
        class MockResponse(object):
            def __init__(self, url=None, headers=None):
                self.url = url
                self.headers = headers

        with mock.patch("logging.Logger.info") as m:
            facebook.GraphAPILogger(
                logger, facebook.LoggingVerbosity.BASIC_REQUEST_INFO
            ).log_response(MockResponse(url="x", headers="y"))
            assert m.call_args_list == [
                mock.call("Response URL: x"),
                mock.call("Response Headers: y"),
            ]

    def test_log_error(self):
        err = facebook.GraphAPIError({})
        err.code = "400"
        err.error_subcode = "100"
        err.headers = "headers"
        err.method = "GET"
        err.url = "url"
        with mock.patch("logging.Logger.info") as m:
            facebook.GraphAPILogger(
                logger, facebook.LoggingVerbosity.ON_EXCEPTION_ONLY
            ).log_error(err)
            assert m.call_args_list == [
                mock.call("GraphAPIError code: 400"),
                mock.call("GraphAPIError error_subcode: 100"),
                mock.call("GraphAPIError headers: headers"),
                mock.call("GraphAPIError method: GET"),
                mock.call("GraphAPIError url: url"),
            ]
