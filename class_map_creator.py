#!/usr/bin/python3

import drivers.class_base_map_driver as bm

import sys
import unittest

debug = True

class Map:

    def __init__(self, MapDriver):

        self.__MapDriver = MapDriver

        self.__connectors = []

        self.__draw_history = []

        self.__maze_length = 0

        self.__maze_width = 0

    def getDrawHistory(self):

        return self.__draw_history

    def ReadMap(self, filename):

        with open(filename, "r") as map:
            
            current_line = 0

            self.__draw_history = []

            while True: 
                line = map.readline().strip()

                if debug:
                    print("\nLine ", current_line,": ", line  )

                if line == '':
                    break

                if current_line % 2 == 0:
                    # even line, horizontal wall

                    # reset connector list for odd lines
                    self.__connectors = []

                    wall_chars = 0

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
                            self.__MapDriver.WriteHorizontalWall( line_index, column_index ); 
                            self.__draw_history.append( ( "H", line_index, column_index) )

                            # this variable holds the current width of the wall 
                            wall_chars += 1

                            column_index += 1
                        elif character == ' ':
                            # open wall, do nothing
                            wall_chars += 1

                            column_index += 1

                        elif character == 'O':
                            # empty connector, do nothing
                            pass
                            
                        else:

                            sys.stderr.write("\n[WARN] Invalid character (" +\
                                 character +\
                                 ") on line " +\
                                 str(current_line) )

                        last_char = character

                    if current_line == 0:
                        # first line defines the maze width
                        self.__maze_length = wall_chars
                    else:
                        # all other lines must match the number calculated above
                        if self.__maze_length != wall_chars:
                            msg = "Line {0} has width {1}, expected {2}!".\
                                format( current_line, wall_chars, self.__maze_length )
                            raise ValueError(msg)

                else:                    
                    if len(line) == 0:
                        msg = "Line {0} empty, expected column line"
                        raise ValueError( msg.format( current_line ) )

                    expected_walls = len( self.__connectors )
                    returned_walls = 0

                    # checking for valid characters

                    for element in range( len(line) ):
                        character = line[element]
                        if character == '|':
                            # vertical line character, add to expected walls
                            returned_walls += 1
                            continue
                        elif character == ' ':
                            continue
                        else:
                            msg = "Line {0}: expected '|' or empty space, got '{1}'"
                            raise ValueError (msg.format( current_line, character ) )

                    if returned_walls != expected_walls :
                        msg = "Line {0}: expected {1} '|''s, got {2}"
                        raise ValueError (msg.format( current_line, expected_walls, returned_walls ) )                        

                    # odd line, vertical walls
                    while len( self.__connectors ) > 0:
                        coordinates = self.__connectors.pop(0)

                        x = coordinates[ 0 ]
                        y = coordinates[ 1 ]

                        self.__MapDriver.WriteVerticalWall( x, y )
                        self.__draw_history.append( ( "V", x, y ) )

                    self.__maze_width += 1                  

                current_line += 1

    def BuildMap( self ):
        self.__MapDriver.SetMazeLength( self.__maze_length )
        self.__MapDriver.SetMazeWidth( self.__maze_width )
        self.__MapDriver.BuildMap()
