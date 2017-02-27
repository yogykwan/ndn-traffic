#!/usr/bin/python2
import os
import sys
import glob
import inspect
import unittest
from sets import Set

def usage(testCases):
    print "\nUSAGE:"
    print "  ./run_tests.py [OPTIONS]\n"
    print "  Run a subset of NFD integration test cases"
    print "  The test case(s) to be executed should be provided as command line option(s)"
    print "\nOPTIONS:"
    for testCase in testCases:
        print "  " + testCase
    print "  test_all           - run all the above tests"
    print "  help               - print this message and exit\n"


def main():
    cmd_subfolder = os.path.realpath(
        os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0], "library_helpers")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    validOptions = [ "test_all",
                     "help" ]
    testCases = glob.glob('test_*')
    validOptions.extend(testCases)

    if len(sys.argv) > 1:
        actionList = Set(sys.argv[1:])
        optionStatus = 0
        for action in actionList:
            if action not in validOptions:
                print "Invalid option provided - " + action
                optionStatus = -1
                break
        if optionStatus == 0 and "help" not in actionList:
            if "test_all" in actionList:
                actionList.remove("test_all")
                actionList = Set(testCases)
            suiteList = []
            for action in actionList:
                cmd_subfolder = os.path.realpath(
                    os.path.abspath(os.path.join(os.path.split(
                        inspect.getfile(inspect.currentframe()))[0], action)))
                if cmd_subfolder not in sys.path:
                    sys.path.insert(0, cmd_subfolder)
                suiteList.append(
                    unittest.defaultTestLoader.loadTestsFromName(action + "." + action))
            mainSuite = unittest.TestSuite(suiteList)
            unittest.TextTestRunner().run(mainSuite)
        else:
            usage(testCases)
    else:
        usage(testCases)


if __name__ == "__main__":
    main()
