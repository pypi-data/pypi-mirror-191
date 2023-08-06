# Teamscale Robot Plugin

A plugin that allows integration into the RobotFramework in order to allow testwise coverage recording for TIA.

## How it works

RobotFramework offers a [listener interface](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface) which can be specified via the `--listener` option.
Certain methods can be defined and will be called by RobotFramework at the appropiate time, e.g. `start_test` before a test is started and `end_test` after a test has ended.
The listener also receives a `data` and a `result` parameter in each function that contains information about the test suite and the results, depending on the callback function.
`TiaRobotListener` then invokes the `AgentConnector` which notifies the profiler when a test starts and ends, as well as when a test suite ends.

## Usage

See the [PyPI_README](./PyPI_README.md)

## Local Testing

You can install this package by running `install_plugin.sh` or `install_plugin.bat` in the root directory of this project.
This will uninstall any existing instance of the plugin and install the new version based on this repo.

To start the test suite do

```bash
cd test
./run_test_suite.sh
```

This will start the SUT (Digitalbank), the `AgentStub` (a mock of the JaCoCo Agent) and then run a sample Robotframework test suite to generate coverage.
The `AgentStub` will display all incoming `POST` requests and then validate them after the test suite has ended.

## Publishing

First, you must increase the version number in `./pyproject.toml`.
PyPI prevents re-uploading packages with the same version number _even if you delete the old package in the PyPI web interface_!

To publish the package, you'll need the access token for PyPI from 1password's _Teamscale Build + Release_ vault (the release crew has access).
There's a different token, depending on whether you want to test publishing or publish for real:

- For testing: _TestPyPI Account for RobotFramework Plugin_
- For production: _PyPI Account for RobotFramework Plugin_

Then, run `./publish.sh` and enter the testing access token.
This will publish the package to <https://test.pypi.org/project/teamscalerobotplugin/>.
Install the package from this site and make sure it works.

Then deploy it to the real PyPI with `./publish.sh --prod`, using the production access token.

