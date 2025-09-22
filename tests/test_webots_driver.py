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

    def test_00_start(self):

        unittest.SkipTest()

    def test_01_map_generation(self):

        shutil.rmtree("./__testing/", ignore_errors=True)

        os.mkdir("__testing")

        for map in sorted( os.listdir("./maps") ):
            print("Generating" , map , " ...")

            proc= sp.run( [ './main.py', '-i',  './maps/' + map ] ,\
                stdout = sp.DEVNULL ,\
                stderr = sp.STDOUT )

            self.assertEqual( proc.returncode , 0 )

            shutil.move( "output" ,"__testing/" + map[ : map.index(".txt") ] )

    def test_02_controller_compilation(self):
            
        cur_dir = os.getcwd()

        for proj in sorted( os.listdir("./__testing") ):
            print( "Compiling " , proj, "controller ..." )

            os.chdir( cur_dir + "/__testing/" + proj + "/controllers/four_wheels_collision_avoidance" )

            proc = sp.run( ['make', 'WEBOTS_HOME=/usr/local/webots', 'clean' ] ,\
                stdout = sp.DEVNULL ,\
                stderr = sp.STDOUT )
            
            self.assertEqual( proc.returncode, 0 )            

            proc = sp.run( ['make', 'WEBOTS_HOME=/usr/local/webots', 'all' ] ,\
                stdout = sp.PIPE ,\
                stderr = sp.STDOUT )
            
            self.assertEqual( proc.returncode, 0 )

            with open( 'build.log' , 'w' ) as log:
                log.write( str(proc.stdout ) ) 



if __name__ == '__main__' :

    unittest.main()                