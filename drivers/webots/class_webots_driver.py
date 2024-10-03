#!/usr/bin/python3

import sys

from string import Template

sys.path.append('../')

sys.path.append('./drivers')

sys.path.append('.')

debug = True

import class_base_map_driver as bmd

class WebotsDriver( bmd.BaseMapDriver ):

    def __init__(self, map_name ):

        try:

            map_file = open(map_name, "w")

        except Exception as e:

            sys.stderr.write ( "[WebotsDriver] ERROR:" +  e )

            return

        self.__walls = ''

        self.__total_width = 0

        self.__total_height = 0

        self.__wall_width = 1

        self.__wall_height = 1

        # index 1 is wall shape from which all other walls will inherit
        self.__wall_index = 2

        with open("./drivers/webots/wall_model_horizontal.txt", "r" ) as wall_model_h_f:

            self.wall_model_hor = Template( wall_model_h_f.read() )

        with open("./drivers/webots/wall_model_vertical.txt", "r" ) as wall_model_v_f:

            self.wall_model_ver = Template( wall_model_v_f.read() )

        with open("./drivers/webots/wall_shape.txt", "r" ) as wall_shape_f:

            self.wall_model_shape = Template( wall_shape_f.read() )

        with open("./drivers/webots/floor_model.txt", "r" ) as floor_model_f:

            self.floor_model = Template( floor_model_f.read() )

        with open("./drivers/webots/header.txt", "r" ) as header_f:

            self.header = Template( header_f.read() )

        with open("./drivers/webots/robot.txt", "r" ) as robot_f:

            self.robot = Template( robot_f.read() )            

        if debug:

            x = self.wall_model_hor.substitute( n = 0, x = 1, y = 2, z = 3 )

            sys.stderr.write( x )

    def __write_wall(self):
        pass

    def WriteHorizontalWall(self, x_i, y_i, z_i = 0):
        sys.stderr.write("\n[WebotsDriver] WriteHorizontalWall( {0}, {1} )"\
            .format( x, y ) )

        trans_x = x_i * self.__wall_width

        trans_y = y_i * self.__wall_height

        trans_z = z_i * 0

        self.__walls += self.wall_model_hor.substitute( \
            x = trans_x, \
            y = trans_y, \
            z = trans_z, \
            n = self.__wall_index )

        self.__wall_index += 1

    def WriteVerticalWall(self, x, y, z  = 0):
        sys.stderr.write("\n[WebotsDriver], WriteVerticalWall( {0}, {1} )"\
            .format( x, y ) )
        pass

    def WriteFloor(self, x, y, width, height):
        pass