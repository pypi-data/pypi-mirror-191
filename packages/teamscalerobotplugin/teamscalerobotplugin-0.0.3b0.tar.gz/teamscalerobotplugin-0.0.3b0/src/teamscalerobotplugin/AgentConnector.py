from urllib.parse import quote
import requests
import logging


class AgentConnector:
    """Provides functionality to interact with the agent that records the test coverage."""

    def __init__(self, url):
        self._url = self._parse_url(url)
        self._logger = logging.getLogger(__package__)

    def tia_start_test(self, test):
        """Notify the agent that a test is about to start."""
        self._request("test/start/" + quote(test, safe=""))

    def tia_end_test(self, test, result, message=""):
        """Notify the agent that a test has ended"""
        self._request("test/end/" + quote(test, safe=""),
                      {"result": result, "message": message})

    def tia_start_testrun(self, available_tests):
        """Notify the agent that a test run is about to start. 
        The provided available tests will be used to select the impacted tests.
        Returns a cluster containing impacted tests."""
        self._logger.debug(
            "Available tests: %s", available_tests)
        impacted_tests = self._request("testrun/start", available_tests)
        self._logger.debug(
            "Received impacted tests: %s", impacted_tests)
        return impacted_tests

    def tia_end_testrun(self):
        """Notify the agent that the test run has ended."""
        self._request("testrun/end")

    def _request(self, path, json=None):
        url = self._url + path
        self._logger.debug("Posting to %s", url)
        self._logger.debug("Request body %s", json)
        try:
            response = requests.post(url, json=json)
            if response.ok:
                self._logger.debug("Request successful")
                return response.content.decode()
            else:
                self._logger.error("Request failed: %s\n-----\n%s\n-----", str(response.status_code), response.text)
                return None
        except Exception as e:
            self._logger.error("Request failed: %s", str(e))
            return None

    def _parse_url(self, url: str):
        """Ensures that URLs end with '/'"""
        return url if url.endswith('/') else url + '/'
