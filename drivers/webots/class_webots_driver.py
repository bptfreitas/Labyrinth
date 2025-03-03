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

            self.map_file = open( map_name, "w")
            
            self.MAS_file = open( map_name + ".chon", "w")

        except Exception as e:

            sys.stderr.write ( "[WebotsDriver] ERROR:" +  e )

            return
            
        try:
            self.__project_name = map_name[ : map_name.index( '.' ) ]
        except:
            self.__project_name = map_name

        self.__walls = ''

        self.__wall_length = 0

        self.__total_width = 0

        self.__wall_length = 1

        self.__wall_width = 1

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

        with open("./drivers/webots/target.txt", "r" ) as target_f:

            self.target = Template( target_f.read() )
            
        with open("./drivers/webots/charger.model", "r" ) as charger_f:

            self.charger = Template( charger_f.read() )
            
        with open("./drivers/webots/MAS.model", "r" ) as MAS_f:

            self.MAS = Template( MAS_f.read() )
            
        self.__MAS_Beliefs = ''

        if debug:

            x = self.wall_model_hor.substitute( n = 0, x = 1, y = 2, z = 3 )

            sys.stderr.write( x )

    def __write_wall(self):
        pass

    def WriteHorizontalWall(self, x_i, y_i, z_i = 0):
        sys.stderr.write("\n[WeBots Driver] WriteHorizontalWall( {0}, {1} )"\
            .format( x_i, y_i ) )

        trans_x = x_i * self.__wall_length

        trans_y = y_i * self.__wall_width

        trans_z = 0.05

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

    def WriteVerticalWall(self, x_i, y_i, z_i  = 0):
        sys.stderr.write("\n[WeBots Driver] WriteVerticalWall( {0}, {1} )"\
            .format( x_i, y_i ) )

        trans_x = (x_i ) * self.__wall_length  + 0.5

        trans_y = (y_i ) * self.__wall_width - 0.5

        trans_z = 0.05

        self.__walls += self.wall_model_ver.substitute( \
            x = trans_x, \
            y = trans_y, \
            z = trans_z, \
            n = self.__wall_index )

        self.__wall_index += 1 

    def WriteFloor(self, x, y, width, height):
        pass

    def SetMazeLength( self, length):
        sys.stderr.write("\n[WeBots Driver] SetLength( {0} )"\
            .format( length ) )

        self.__total_length = length

    def SetMazeWidth( self, width):
        sys.stderr.write("\n[WeBots Driver] SetWidth( {0} )"\
            .format( width ) )

        self.__total_width = width
        
        
    def SetCharger( self, x_i, y_i, z_i = 0.05):
        sys.stderr.write("\n[WeBots Driver] SetCharger( {0}, {1} )"\
            .format( x_i, y_i ) )

        trans_x = ( x_i ) * self.__wall_length  + 0.5

        trans_y = ( y_i ) * self.__wall_width - 0.5

        trans_z = 0.05
        
        self.__MAS_Beliefs += 'charger1( {0}, {1}, {2} ).\\n\\n'.format( x_i, y_i, z_i )

        self.__charger = self.charger.substitute( x = x_i, y = y_i, z = z_i)

        # self.__tx = - x_i
        # self.__ty = - y_i
        # self.__tz = - z_i

        self.__tx = 0
        self.__ty = 0
        self.__tz = 0        

    def SetTarget( self, x_i, y_i, z_i = 0.05):
        sys.stderr.write("\n[WeBots Driver] SetTarget( {0}, {1} )"\
            .format( x_i, y_i ) )

        trans_x = ( x_i ) * self.__wall_length  + 0.5

        trans_y = ( y_i ) * self.__wall_width - 0.5

        trans_z = 0.05
                        
        self.__MAS_Beliefs += 'target1( {0}, {1}, {2} ).\\n\\n'.format( x_i, y_i, z_i )

        self.__target = self.target.substitute( x = x_i, y = y_i, z = z_i)

        # self.__tx = - x_i
        # self.__ty = - y_i
        # self.__tz = - z_i

        self.__tx = 0
        self.__ty = 0
        self.__tz = 0



    def BuildMap(self):

        header = self.header.substitute( tx = self.__tx ,\
            ty = self.__ty ,\
            tz = 0)

        self.map_file.write( header )

        floor_x = (self.__total_width / 2) 
 
        floor_y = (self.__total_length / 2) - 0.5

        floor = self.floor_model.substitute( \
            x = floor_x,\
            y = floor_y,\
            length = self.__total_length,\
            width = self.__total_width )

        self.map_file.write( floor )

        for wall in self.__walls:
            self.map_file.write( wall )

        self.map_file.write( self.__target )
        
        self.map_file.write( self.__charger )

        robot = self.robot.substitute()

        self.map_file.write( robot )

        self.map_file.close()
        
        
        self.MAS_file.write( self.MAS.substitute( proj_name = self.__project_name , BELIEFS = self.__MAS_Beliefs ) )
        self.MAS_file.close()
        
        

        
