#  _  __         _          ___       _               ___ _           _
# | |/ /_ _ __ _| |_ ___ __/ __| __ _| |___ _ __  ___| _ \ |_  _ __ _(_)_ _
# | ' <| '_/ _` |  _/ _ (_-<__ \/ _` | / _ \ '  \/ -_)  _/ | || / _` | | ' \
# |_|\_\_| \__,_|\__\___/__/___/\__,_|_\___/_|_|_\___|_| |_|\_,_\__, |_|_||_|
#                                                               |___/
# License: BSD License ; see LICENSE
#
# Main authors: Philipp Bucher
#

# python imports
import unittest, sys, os

if __name__ == '__main__':
    print("\nPRINTING INFO about LD_LIBRARY_PATH")
    print("LD_LIBRARY_PATH in os.environ", "LD_LIBRARY_PATH" in os.environ)
    print("os.environ[LD_LIBRARY_PATH]")
    if LD_LIBRARY_PATH" in os.environ:
        for p in sorted(os.environ["LD_LIBRARY_PATH"].split(":")):
            print(p)

    print("FINISHED PRINTING INFO about LD_LIBRARY_PATH\n")

    verbosity = 0
    if len(sys.argv) == 2: # verbosity lvl was passed
        verbosity = int(sys.argv[1])
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.dirname(__file__)) # automatically discover all tests in this directory
    testRunner = unittest.runner.TextTestRunner(verbosity=verbosity)
    result = testRunner.run(tests).wasSuccessful()
    sys.exit(not result) # returning inverse bcs for sys.exit 1 aka true means error
