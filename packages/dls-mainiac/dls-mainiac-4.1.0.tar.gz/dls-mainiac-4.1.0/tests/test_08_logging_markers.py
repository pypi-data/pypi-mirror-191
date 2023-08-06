import argparse
import logging
import os
import shutil

import pytest

# Class under test.
from dls_mainiac_lib.mainiac import Mainiac

logger = logging.getLogger(__name__)


class Test_08_logging_markers:

    # ----------------------------------------------------------------------------------------
    def test(
        self,
        constants,
        logging_setup,
        output_directory,
        capsys,
    ):
        """
        Test mainiac base class.
        """

        failure_message = None
        try:

            # Instantiate the app class.
            app = _App(output_directory)

            # Configure the app from empty command line arguments.
            app.parse_args_and_configure_logging([])

            # Run the gui wrapped in a try/catch.
            app.try_run_catch()

        except Exception as exception:
            logger.exception("unexpected exception during the test", exc_info=exception)
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)


# ---------------------------------------------------------------------------------
class _App(Mainiac):
    """
    App class.
    """

    def __init__(
        self,
        output_directory,
    ):

        program_name = "test_08_logging_markers"

        self.__logfile_directory = f"/tmp/logs/{program_name}"

        if os.path.isdir(self.__logfile_directory):
            shutil.rmtree(self.__logfile_directory)

        Mainiac.__init__(self, program_name)

    # ----------------------------------------------------------
    def run(self):
        logger.debug("[MARKER1] this is marker1")
        logger.debug("[MARKER2] this is marker2, should not appear in logfile")
        logger.debug("[MARKER3] this is marker3, should not appear in logfile")

        filename = "logform.log"
        filename = f"{self.__logfile_directory}/{filename}"

        # Check the logfile got written.
        assert os.path.exists(filename)

        # Check there is the right number of output lines.
        with open(filename, "r") as stream:
            lines = stream.readlines()
            assert len(lines) == 1
            assert "marker1" in lines[0]

    # --------------------------------------------------------------------------
    def configure_logging(self, settings=None):
        """
        Configure runtime logging, override base class.
        Presume that self._args is already set.
        """

        settings = {
            "logfile": {
                "enabled": True,
                "filters": {"markers": ["[MARKER2]", "[MARKER3]"]},
            }
        }
        # Call the base method which has the extra kwarg.
        Mainiac.configure_logging(self, settings)

    # ----------------------------------------------------------
    def version(self):
        return "x.y.z"

    # ----------------------------------------------------------
    def about(self):
        return {"url": "/some/good/url", "description": "A good description"}

    # ----------------------------------------------------------
    def build_parser(self, arglist=None):

        # Make a parser.
        parser = argparse.ArgumentParser()

        # Return a structure describing the default subcommand.
        return parser
