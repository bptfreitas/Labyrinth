#!/usr/bin/python3

import sys
import shutil
import os
import subprocess

sys.path.append('.')

import class_map_creator as mc
import drivers.class_base_map_driver as bm
import drivers.webots.class_webots_driver as webots

import class_map_creator as mc

import argparse
import pathlib

parser = argparse.ArgumentParser()

parser.add_argument('-i', 
    nargs = 1, 
    type = pathlib.Path,
    dest = 'map_filename')

parser.add_argument('-o', 
    nargs='?', 
    type = pathlib.Path,
    dest = 'sim_filename')

args = parser.parse_args( )

print( args.map_filename[0] )

try:
    mapfile = args.map_filename[0]

    with open( mapfile ,  "r") as tmp:
        pass

except Exception as inst:

    print( "Error reading input filename: ", inst )
    
    sys.exit( -1 )

try:

    output_filename =  args.sim_file[0] 

    with open( output_filename, "w") as tmp:
        pass

except Exception as inst:

    output_filename = "world.wbt"

    print( inst )

if not os.path.isdir( "project_model" ):
    print("Downloading project model from github ...")

    cmd = [ ]
    cmd.append( "git" )
    cmd.append( "clone" )
    cmd.append( "https://github.com/bptfreitas/FourWheels_With_ChonIDE_Webots.git" )
    cmd.append( "project_model")

    subprocess.run( cmd )

if os.path.isdir( "output" ):
    shutil.rmtree( "./output" )

shutil.copytree( "project_model" , "output" )

shutil.rmtree( "./output/SMA" )
shutil.rmtree( "./output/worlds" )

os.mkdir( "./output/SMA" )
os.mkdir( "./output/worlds" )

mapDriver = webots.WebotsDriver(output_filename)

map = mc.Map( mapDriver )

print( "Reading map description ...")
map.ReadMap( mapfile )

print( "Buiding map on Webots ..." )
map.BuildMap()

shutil.move( output_filename , "./output/worlds/.")
shutil.move( output_filename + ".chon" , "./output/SMA/.")

