#!/usr/bin/python3

import sys

sys.path.append('.')

import class_map_creator as mc
import drivers.class_base_map_driver as bm
import drivers.webots.class_webots_driver as webots

import class_map_creator as mc

dir( bm )
dir( mc )

mapDriver = webots.WebotsDriver("teste.wbt")

map = mc.Map( mapDriver  )

map.ReadMap("./map.txt")

map.BuildMap()

