Test Case - ndntraffic
======================

## Objective ##

To test the ndn-traffic-generator application on a single host.

## Description ##

This test case will run NFD, ndn-traffic and ndn-server.
This will report SUCCESS if one interest/data is successfully exchanged without any data inconsistency between ndn-traffic and ndn-server.
In all other scenarios, the test case will report FAILURE
