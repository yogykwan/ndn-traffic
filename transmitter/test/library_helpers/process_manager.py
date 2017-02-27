#!/usr/bin/python2
# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 University of Arizona
# Author: Jerald Paul Abraham <jeraldabraham@email.arizona.edu>
# See COPYING for copyright and distribution information.
#

import time
import errno
import subprocess
import multiprocessing as mp

class ProcessManager:

    manager = mp.Manager()
    processes = dict()
    subprocesses = manager.dict()
    results = manager.dict()

    def cleanupProcesses(self):
        self.processes.clear()
        self.subprocesses.clear()
        self.results.clear()

    def runProcess(self,
                   processKey,
                   processCallFormat,
                   message,
                   subprocesses,
                   results,
                   inputFile,
                   outputFile):
        print message
        stdin = None
        if inputFile is not None:
            stdin = open(inputFile, "r")
        stdout = subprocess.PIPE
        if outputFile is not None:
            stdout = open(outputFile, "w")
        process = subprocess.Popen(
            processCallFormat,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE)
        subprocesses[processKey] = process
        try:
            stdout, stderr = process.communicate()
            returnCode = process.returncode
            results[processKey] = (returnCode, stdout, stderr)
        except IOError as e:
            print e
            pass

    def startProcess(self,
                     processKey,
                     processCallFormat,
                     message,
                     inputFile=None,
                     outputFile=None):
        self.processes[processKey] = mp.Process(
            target=self.runProcess,
            args=[processKey,
                  processCallFormat,
                  message,
                  self.subprocesses,
                  self.results,
                  inputFile,
                  outputFile])
        self.processes[processKey].start()

    def killProcess(self, processKey):
        if processKey not in self.results and processKey in self.subprocesses:
            subprocess.call(['sudo', 'kill', str(self.subprocesses[processKey].pid)])

    def hasProcessCompleted(self, processKey):
        if processKey in self.results:
            return True
        else:
            return False

    def waitForProcessCompletion(self, processKey, waitTime):
        self.processes[processKey].join(waitTime)

    def getProcessReturnCode(self, processKey):
        if processKey in self.results:
            (returnCode, stdout, stderr) = self.results[processKey]
            return returnCode
        else:
            print "Invalid processKey provided - " + processKey
            return -1

    def getProcessError(self, processKey):
        if processKey in self.results:
            (returnCode, stdout, stderr) = self.results[processKey]
            return stderr
        else:
            return "Error not available for processKey - " + processKey

    def getProcessOutput(self, processKey):
        if processKey in self.results:
            (returnCode, stdout, stderr) = self.results[processKey]
            return stdout
        else:
            return "Output not available for processKey - " + processKey

    def startNfd(self):
        self.startProcess("nfd", ["sudo", "nfd"], "-> Starting NFD")

    def killNfd(self):
        self.killProcess("nfd")
        time.sleep(2)
