import json
import logging
import sys

from teamscalerobotplugin.RobotTestFinder import RobotTestFinder
from teamscalerobotplugin.AgentConnector import AgentConnector
from teamscalerobotplugin.UniformPathUtil import get_uniform_path

from robot.api import logger

class TiaRobotListener:
    """Uses RobotFramework's listener interface. Passed to RobotFramework via the --listener keyword."""

    # The Robot listener API version that should be used.
    # Version 3 can modify all RobotFramework internal data structures, e.g. for selecting impacted tests. 
    # See http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface-methods for details
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, partition, url="http://localhost:7001/", log_file="./teamscale-robot-plugin.log", log_level="INFO") -> None:
        self._agent_connector = AgentConnector(url)
        """The partition to use when querying the agent for impacted tests"""
        self.__partition = partition
        """The connector that is responsible for communicating with the JaCoCo Agent"""
        self._available_tests = []
        """A list of the uniform paths of all available tests"""
        self._path = []
        """The uniform path of the current test suite"""
        self._impacted_tests = []
        """A list of the uniform paths of all impacted tests"""
        self._logger = self._init_logging(log_file, log_level)


    def start_suite(self, data, result):
        """Called before a test suite starts. Retrieve impacted tests and perform test selection."""
        self._path.append(data.name)
        if data.parent is None:
            # Collect all available test cases in the root suite and use them to query for impacted tests
            self._available_tests = RobotTestFinder.get_available_tests(data)
            self._impacted_tests = self._get_impacted_tests()
            self._logger.info("Running %i/%i impacted tests", len(self._impacted_tests), len(self._available_tests))
            self._logger.debug("Using impacted tests: %s", self._impacted_tests)

        data.tests[:] = [test for test in data.tests if get_uniform_path(self._path, test.name) in self._impacted_tests]
        if not data.has_tests:
            data.setup = None

    def end_suite(self, data, result):
        """Called when a suite has ended. Updates the current suite path"""
        self._path.pop()

    def start_test(self, data, result):
        """Called before a test starts. Notifies the Agent"""
        self._agent_connector.tia_start_test(get_uniform_path(self._path, data.name))

    def end_test(self, data, result):
        """Called when a test has ended. Parses the result and forwards it to the Agent"""
        status = ""
        if result.passed:
            status = "PASSED"
        elif result.failed:
            status = "FAILURE"
        elif result.skipped:
            status = "SKIPPED"

        self._agent_connector.tia_end_test(get_uniform_path(self._path, data.name), status, result.message)

    def close(self):
        """Called when the whole test execution ends"""
        self._agent_connector.tia_end_testrun()

    def _get_impacted_tests(self):
        """Retrieves the uniform paths of impacted tests for this test run"""
        available_tests = [{"clusterId": 0, "uniformPath": test, "partition": self.__partition} for test in self._available_tests]
        response = self._agent_connector.tia_start_testrun(available_tests)
        if response is None or response == "":
            self._logger.error("Retrieving the impacted tests failed, fall back to executing all tests")
            return self._available_tests

        impacted_clusters = json.loads(response)
        if len(impacted_clusters) < 1:
            # No impacted tests
            return []

        return [impacted_test["testName"] for impacted_test in impacted_clusters[0]["tests"]]

    def _init_logging(self, log_file, log_level):
        """Setup a new logger for this package as to not interfere with RobotFramework's logging"""
        logger = logging.getLogger(__package__)
        formatter = logging.Formatter(
            '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
        # The stream handler will only output ERRORs to stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        # The file handler will write every log to the file
        file_handler = logging.FileHandler(filename=log_file, mode='a')
        file_handler.setLevel(logging.getLevelName(log_level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.getLevelName(log_level))
        return logger
