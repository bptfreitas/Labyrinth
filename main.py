#!/usr/bin/python3

import sys

sys.path.append('.')

import class_map_creator as mc
import drivers.class_base_map_driver as bm
import drivers.webots.class_webots_driver as webots

import class_map_creator as mc

try:
    mapfile = open(sys.argv[1], "r")

except Exception as inst:

    print( inst )
    
    sys.exit( -1 )

try:

    output_filename =  sys.argv[2] 

    tmp = open(sys.argv[2], "w")

except Exception as inst:

    output_filename = "world.wbt"

    print( inst )

mapDriver = webots.WebotsDriver(output_filename)

map = mc.Map( mapDriver )

map.ReadMap( sys.argv[1] )

map.BuildMap()

