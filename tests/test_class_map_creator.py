#!/usr/bin/python3

import sys
sys.path.append('../')

sys.path.append('.')

import unittest

import class_map_creator as mc

import drivers.class_base_map_driver as bm

class TestMap(unittest.TestCase):

    def test_horizontal_walls_01(self):

        map01_file = "/tmp/test_horizontal_walls_01.txt"
        
        with open(map01_file, "w") as map01:

            map01.write( "--" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        map.ReadMap( map01_file )

        draw_history = map.getDrawHistory()

        self.assertEqual( len(draw_history), 2 )

        self.assertEqual( draw_history[0], ( "H", 0, 0 ) )

        self.assertEqual( draw_history[1], ( "H", 0, 1 ) )

    def test_horizontal_walls_02(self):

        map_file = "/tmp/test_horizontal_walls_02.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "*-" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        map.ReadMap( map_file )

        draw_history = map.getDrawHistory()

        self.assertEqual( len(draw_history), 2 )
        self.assertEqual( draw_history[0], ( "C", 0, 0 ) )
        self.assertEqual( draw_history[1], ( "H", 0, 0 ) )

    def test_horizontal_walls_03(self):

        map_file = "/tmp/test_horizontal_walls_03.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "*-*" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        map.ReadMap( map_file )

        draw_history = map.getDrawHistory()

        self.assertEqual( len(draw_history), 3 )

        self.assertEqual( draw_history[0], ( "C", 0, 0 ) )
        self.assertEqual( draw_history[1], ( "H", 0, 0 ) )
        self.assertEqual( draw_history[2], ( "C", 0, 1 ) )

    def test_horizontal_walls_04(self):

        map_file = "/tmp/test_horizontal_walls_04.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "-*-" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        map.ReadMap( map_file )

        draw_history = map.getDrawHistory()

        self.assertEqual( len(draw_history), 3 )

        self.assertEqual( draw_history[0], ( "H", 0, 0 ) )
        self.assertEqual( draw_history[1], ( "C", 0, 1 ) )
        self.assertEqual( draw_history[2], ( "H", 0, 1 ) )

    def test_sequential_connectors_01(self):

        map_file = "/tmp/test_sequential_connectors_01.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "**" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        self.assertRaises( ValueError, map.ReadMap, map_file )

    def test_empty_column_line_01(self):

        self.skipTest("Must refactor what to do with empty lines")

        map_file = "/tmp/test_empty_column_line_01.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "-\n " )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        self.assertRaises( ValueError, map.ReadMap, map_file )

    def test_expected_number_of_vertical_walls_01(self):

        map_file = "/tmp/test_expected_number_of_vertical_walls.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "-*-*\n|" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        self.assertRaises( ValueError, map.ReadMap, map_file )          

    def test_vertical_wall_01(self):

        map_file = "/tmp/test_vertical_wall_01.txt"
        
        with open(map_file, "w") as map01:

            map01.write( "*\n|" )

        mapDriver = bm.BaseMapDriver()

        map = mc.Map(mapDriver)

        map.ReadMap( map_file )

        draw_history = map.getDrawHistory()

        self.assertEqual( len(draw_history), 2 )
        
        self.assertEqual( draw_history[0], ( "C", 0, 0 ) )
        self.assertEqual( draw_history[1], ( "V", 0, 0 ) )

if __name__ == '__main__' :

    unittest.main()                