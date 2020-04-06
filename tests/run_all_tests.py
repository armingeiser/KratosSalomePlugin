#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher (https://github.com/philbucher)
#

# python imports
import unittest, sys, os

if __name__ == '__main__':
    # no logging should be outputted here, since the logging is initialized directly in "salome_plugins.py"
    # if problems occur the handlers could be removed from the root logger

    # TODO find a better solution for the following:
    # This also affects the individual tests
    sys.path.append(os.pardir) # needed to bring the plugin into the path, e.g. make "import ks_plugin" possible

    os.environ["KS_PLUGIN_TESTING"] = "1" # this disables all logging, see ks_plugin.plugin_logging

    verbosity = 0
    if len(sys.argv) == 2: # verbosity lvl was passed
        verbosity = int(sys.argv[1])
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.dirname(__file__)) # automatically discover all tests in this directory
    testRunner = unittest.runner.TextTestRunner(verbosity=verbosity)
    result = testRunner.run(tests).wasSuccessful()
    sys.exit(not result) # returning inverse bcs for sys.exit 1 aka true means error
