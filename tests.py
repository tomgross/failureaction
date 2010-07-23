import doctest
import unittest

def test_suite():
    """ Return the test suite """
    return unittest.TestSuite([doctest.DocFileSuite('README.txt')])