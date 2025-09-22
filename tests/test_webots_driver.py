#!/usr/bin/python3

import sys

sys.path.append('../')

sys.path.append('.')

import unittest

import class_map_creator as mc

import drivers.webots.class_webots_driver as webots_driver

class TestMap(unittest.TestCase):

    def test_start(self):

        unittest.SkipTest()


if __name__ == '__main__' :

    unittest.main()                