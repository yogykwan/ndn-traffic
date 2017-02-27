#!/usr/bin/python2
# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 University of Arizona
# Author: Jerald Paul Abraham <jeraldabraham@email.arizona.edu>
# See COPYING for copyright and distribution information.
#

import os
import time
import unittest
import process_manager

class test_ndntraffic(unittest.TestCase, process_manager.ProcessManager):
    """Test case for testing ndn-client-transmitter application"""

    def setUp(self):
        print "\nTesting ndn-client-transmitter"
        print "*****************************"

    def tearDown(self):
        self.killNfd()
        self.killProcess("ndn-server")
        self.killProcess("ndn-client")
        self.cleanupProcesses()

    def test_traffic(self):
        self.startNfd()
        time.sleep(1)
        self.startProcess("ndn-server",
            ["ndn-server"],
            "-> Starting Traffic Server")
        time.sleep(1)
        clientConfigurationFile = os.path.abspath("test_ndntraffic/a5000_0.6.conf")
        self.startProcess("ndn-client",
            ["ndn-client", "-i", "100", "-c", "5", "-f", clientConfigurationFile],
            "-> Starting Traffic Client")
        time.sleep(1)
        self.waitForProcessCompletion("ndn-client", 2)
        self.waitForProcessCompletion("ndn-server", 2)
        if self.hasProcessCompleted("ndn-client"):
            if self.getProcessReturnCode("ndn-client") != 0:
                print self.getProcessError("ndn-client")
                self.fail(">> TEST FAILED - received non-zero return code from ndn-client")
        else:
            self.fail(">> TEST FAILED - ndn-client failed to complete")
#        if self.hasProcessCompleted("ndn-server"):
#            if self.getProcessReturnCode("ndn-server") != 0:
#                print self.getProcessError("ndn-server")
#                self.fail(">> TEST FAILED - received non-zero return code from ndn-server")
#        else:
#            self.fail(">> TEST FAILED - ndn-server failed to complete")
#        print ">> TEST SUCCESSFUL"
