import numpy as np
import os
from gcodepy.gcode import Gcode

# Constants
PUSHER_LENGTH = 24
FEEDER_CLEARANCE = 30
FEEDER_WALL = 3.2
TILE_SIZE = 12
HOLE_DISTANCE = 16
SAFE_RANGE = {
    'x': {'MIN':-10, 'MAX':190},
    'y': {'MIN':0.5, 'MAX':215},
    'z': {'MIN':34.6, 'MAX':175}
}
BUILD_DIR = "build/"

def setup(gcode):
     # home print head
    gcode.home()
    gcode.file.write("M420 S1\n")

    # center the print head
    gcode.travel_absolute((89,115,SAFE_RANGE['z']['MIN']))
    gcode.file.write("M0 S10 Press button to continue.\n")

def end(gcode):
    gcode.travel((0,0,FEEDER_CLEARANCE))
    gcode.close()

def despense_tile(gcode, tile_number):
    pass

def square_test(gcode):
    gcode.travel_absolute((SAFE_RANGE['x']['MIN'],SAFE_RANGE['y']['MIN'],SAFE_RANGE['z']['MIN']))
    gcode.travel((0,SAFE_RANGE['y']['MAX']-SAFE_RANGE['y']['MIN'],0))
    gcode.travel((SAFE_RANGE['x']['MAX']-SAFE_RANGE['x']['MIN'],0,0))
    gcode.travel((0,SAFE_RANGE['y']['MIN']-SAFE_RANGE['y']['MAX'],0))
    gcode.travel((SAFE_RANGE['x']['MIN']-SAFE_RANGE['x']['MAX'],0,0))
    # trave diagonally
    gcode.travel((SAFE_RANGE['x']['MAX']-SAFE_RANGE['x']['MIN'],SAFE_RANGE['y']['MAX']-SAFE_RANGE['y']['MIN'],0))

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    g = Gcode(f"{BUILD_DIR}/test.gcode")

    setup(g)
    square_test(g)
    end(g)
    
    # print the gcode to the console
    with open(f"{BUILD_DIR}/test.gcode", "r") as f:
        print(f.read())

    print("Done!")

if __name__ == "__main__":
    main()