#!/usr/bin/python3

import drivers.class_base_driver_map as bm

import sys
import unittest

class Map:

    def __init__(self, BaseMapDriver):

        self.__MapDriver = bm.BaseMapDriver()

        self.__connectors = []

        self.__draw_history = []

    def getDrawHistory(self):

        return self.__draw_history


    def ReadMap(self, filename):

        with open(filename, "r") as map:
            
            current_line = 0

            while True: 
                line = map.readline().strip()

                if line == '':
                    break

                self.__connectors = []
                self.__draw_history = []

                if current_line % 2 == 0:
                    # even line, horizontal bars
                    line_index = current_line / 2

                    column_index = 0

                    last_char = ''

                    for element in range( len(line) ):

                        character = line[ element ]
                        
                        if character == '*':
                            # connector to vertical wall
                            if character == last_char:
                                raise ValueError("Line {0}, Column {1}: can't have 2 connectors in sequence!"\
                                    .format( current_line, column_index) )

                            self.__connectors.append( ( line_index, column_index ) )

                            self.__draw_history.append( ( "C", line_index, column_index ) )                            

                        elif character == '-':
                            # horizontal wall
                            self.__MapDriver.WriteHorizontalWall( ( line_index, column_index ) ); 
                            self.__draw_history.append( ( "H", line_index, column_index) )

                            column_index += 1
                        else:

                            sys.stderr.write("\n[WARN] Invalid character (" +\
                                 character +\
                                 ") on line " +\
                                 str(current_line) )

                        last_char = character

                else:
                    # odd line, vertical bars
                    while len( self.__connectors ) > 0:
                        coordinates = self.__connectors.pop(0)

                        x = coordinates[ 0 ]
                        y = coordinates[ 1 ]

                        self.__MapDriver.WriteVerticalWall( ( x, y ) );
                        self.__draw_history.append( ( "V", x, y ) )                        

                line_index += 1
                print(line)


class TestMap(unittest.TestCase):

    def test_horizontal_walls_01(self):

        map01_file = "/tmp/test_horizontal_walls_01.txt"
        
        with open(map01_file, "w") as map01:

            map01.write( "--" )

        mapDriver = bm.BaseMapDriver()

        map = Map(mapDriver)

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

        map = Map(mapDriver)

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

        map = Map(mapDriver)

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

        map = Map(mapDriver)

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

        map = Map(mapDriver)

        self.assertRaises( ValueError, map.ReadMap, map_file )

    

if __name__ == '__main__' :

    unittest.main()                