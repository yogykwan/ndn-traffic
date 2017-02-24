import random
import bisect
import math
import numpy


def randZipf(n, alpha, numSamples):
    # Calculate Zeta values from 1 to n:
    tmp = numpy.power(numpy.arange(1, n + 1), -alpha)
    zeta = numpy.r_[0.0, numpy.cumsum(tmp)]
    # Store the translation map:
    distMap = [x / zeta[-1] for x in zeta]
    # Generate an array of uniform 0-1 pseudo-random values:
    u = numpy.random.random(numSamples)
    # bisect them with distMap
    v = numpy.searchsorted(distMap, u)
    samples = [str(t - 1) for t in v]
    return samples


def CPA(n):
    samples = ["CPA" + str(i) for i in range(n)]
    return samples


def IFA(n):
    samples = ["IFA" + str(i) for i in range(n)]
    return samples


def store(samples, fileName):
    f = open(fileName, "a+")
    for i in samples:
        f.write(i + " ")
    f.close()

store(randZipf(5000, 0.6, 90000), "conf/a5000_0.6.conf")
store(randZipf(5000, 0.8, 90000), "conf/a5000_0.8.conf")

store(randZipf(10000, 0.8, 90000), "conf/a10000_0.8.conf")
store(randZipf(10000, 0.6, 90000), "conf/a10000_0.6.conf")

store(CPA(60000), "conf/cpa.conf")
store(IFA(60000), "conf/ifa.conf")

store(CPA(30000), "conf/cpa_ifa.conf")
store(IFA(30000), "conf/cpa_ifa.conf")
