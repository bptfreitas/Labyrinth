#!/usr/bin/python3

import sys
import shutil
import os
import subprocess as sp

sys.path.append('../')

sys.path.append('.')

import unittest

import class_map_creator as mc

import drivers.webots.class_webots_driver as webots_driver

class TestMap(unittest.TestCase):

    def test_start(self):

        unittest.SkipTest()

    def test_map_generation(self):

        for map in sorted( os.listdir("./maps") ):
            print(map)

            proc= sp.run( [ './main.py', '-i',  './maps/' + map ] ,\
                stdout = sp.DEVNULL ,\
                stderr = sp.STDOUT )

            self.assertEqual( proc.returncode , 0 )


if __name__ == '__main__' :

    unittest.main()                