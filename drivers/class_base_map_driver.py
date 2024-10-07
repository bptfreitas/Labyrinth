#!/usr/bin/python3

import sys

class BaseMapDriver:

    def __init__(self):

        self.__wall_width = 1

        self.__wall_height = 1

    def __write_wall(self):
        pass

    def WriteHorizontalWall(self, point2D ):
        sys.stderr.write("\nWriteHorizontalWall( {0}, {1} )"\
            .format( point2D[0], point2D[1] ) )

        pass

    def WriteVerticalWall(self, point2D):
        sys.stderr.write("\nWriteVerticalWall( {0}, {1} )"\
            .format( point2D[0], point2D[1] ) )
        pass

    def WriteFloor(self, x, y, width, height):
        pass

    def BuildMap(self ):
        pass