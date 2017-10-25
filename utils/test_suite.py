#-*- coding=utf-8 -*-

import unittest
from utils.test_func import TestDatabase

if __name__ == "__main__":
    suite = unittest.TestSuite()
    tests = [TestDatabase("test_mysqlPool")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
