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

            self.map_file = open(map_name, "w")

        except Exception as e:

            sys.stderr.write ( "[WebotsDriver] ERROR:" +  e )

            return

        self.__walls = ''

        self.__total_width = 0

        self.__total_height = 0

        self.__wall_width = 1

        self.__wall_height = 1

        # index 1 is wall shape from which all other walls will inherit
        self.__wall_index = 1

        with open("./drivers/webots/wall_model_horizontal.txt", "r" ) as wall_model_h_f:

            self.wall_model_hor = Template( wall_model_h_f.read() )

        with open("./drivers/webots/wall_model_vertical.txt", "r" ) as wall_model_v_f:

            self.wall_model_ver = Template( wall_model_v_f.read() )

        with open("./drivers/webots/wall_shape.txt", "r" ) as wall_shape_f:

            self.wall_shape = Template( wall_shape_f.read() )

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
            .format( x_i, y_i ) )

        trans_x = x_i * self.__wall_width

        trans_y = y_i * self.__wall_height

        trans_z = 0

        if self.__wall_index == 1:
            # wall shape

            self.__walls += self.wall_shape.substitute( \
                x = trans_x, \
                y = trans_y, \
                z = trans_z, \
                n = self.__wall_index )

        else:

            self.__walls += self.wall_model_hor.substitute( \
                x = trans_x, \
                y = trans_y, \
                z = trans_z, \
                n = self.__wall_index )

        self.__wall_index += 1

        self.__total_width += self.__wall_width

    def WriteVerticalWall(self, x_i, y_i, z_i  = 0):
        sys.stderr.write("\n[WebotsDriver], WriteVerticalWall( {0}, {1} )"\
            .format( x_i, y_i ) )

        trans_x = (x_i ) * self.__wall_width  + 0.5

        trans_y = (y_i ) * self.__wall_height - 0.5

        trans_z = 0

        self.__walls += self.wall_model_ver.substitute( \
            x = trans_x, \
            y = trans_y, \
            z = trans_z, \
            n = self.__wall_index )

        self.__wall_index += 1

        self.__total_height += self.__wall_height

    def WriteFloor(self, x, y, width, height):
        pass

    def BuildMap(self):

        header = self.header.substitute()

        self.map_file.write( header )

        floor = self.floor_model.substitute( \
            width = self.__total_width,\
            height = self.__total_height )

        self.map_file.write( floor )

        for wall in self.__walls:
            self.map_file.write( wall )

        robot = self.robot.substitute()

        self.map_file.write( robot )

        self.map_file.close()

        