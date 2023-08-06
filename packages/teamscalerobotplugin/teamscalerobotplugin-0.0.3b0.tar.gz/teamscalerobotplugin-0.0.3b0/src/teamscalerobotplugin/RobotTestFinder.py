from robot.model import SuiteVisitor

from teamscalerobotplugin.UniformPathUtil import get_uniform_path

class RobotTestFinder(SuiteVisitor):
    """Finds and collects the uniform paths of all available test cases for TIA"""

    def __init__(self):
        self._path = []
        self._tests = []

    def start_suite(self, suite):
        """Add this suite's name to the uniform path"""
        self._path.append(suite.name)

    def end_suite(self, suite):
        """Remove this suite's name from the uniform path"""
        self._path.pop()

    def visit_test(self, test):
        """Called on each test case"""
        self._tests.append(get_uniform_path(self._path, test.name))

    @staticmethod
    def get_available_tests(test_suite):
        """Collect uniform paths of all test cases in the suite using the visitor pattern."""
        test_finder = RobotTestFinder()
        test_suite.visit(test_finder)
        return test_finder._tests
