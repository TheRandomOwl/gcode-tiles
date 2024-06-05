"""
GCODE info: https://marlinfw.org/meta/gcode/
"""
import os
from gcodepy.gcode import Gcode

# Constants
PUSHER_LENGTH = 24
FEEDER_CLEARANCE = 30
FEEDER_WALL = 3.2
HOLE_SIZE = 12
HOLE_DISTANCE = 16
SAFE_RANGE = {
    'x': {'MIN':-10, 'MAX':190},
    'y': {'MIN':9, 'MAX':215},
    'z': {'MIN':34.6, 'MAX':175}
}
# Adjust x and y as needed
DESPENSER_COORD = (187.1,160,SAFE_RANGE['z']['MIN'])
BUILD_DIR = "build/"

MOSSAIC = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4]
]

def setup(gcode):
     # home print head skip z if already homed to save time
    gcode.file.write("G28 X Y\n")
    gcode.file.write("G28 O\n")
    gcode.file.write("M420 S1\n")

    # center the print head
    gcode.travel_absolute((89,115,SAFE_RANGE['z']['MIN']))
    gcode.file.write("M0 S10 Press button to continue.\n")

def end(gcode):
    gcode.travel((0,0,FEEDER_CLEARANCE))
    gcode.close()

def despense_tile(gcode, tile_index):
    """
    Move x and y to the despenser side before using this function
    Moves the print head to the despenser and despenses a tile
    """
    gcode.travel_absolute((DESPENSER_COORD[0], DESPENSER_COORD[1]-tile_index*HOLE_DISTANCE, SAFE_RANGE['z']['MIN']))
    gcode.travel((-PUSHER_LENGTH,0,0), feedrate=1000)
    gcode.travel((PUSHER_LENGTH,0,0), feedrate=1000)

def move_to_mossaic(gcode, row, col):
    """
    Moves the print head to the mossaic and places the tile
    Run after despense_tile
    """
    gcode.travel((0,0,FEEDER_CLEARANCE))
    # Move print head over feeder
    gcode.travel((-(PUSHER_LENGTH+2*FEEDER_WALL+HOLE_SIZE+3.3),0,0))
    gcode.travel_absolute((gcode.get_x(),gcode.get_y()+HOLE_DISTANCE,SAFE_RANGE['z']['MIN']))

    # Move print head to mossaic
    gcode.travel_absolute((SAFE_RANGE['x']['MIN']+col*HOLE_DISTANCE,SAFE_RANGE['y']['MIN']+row*HOLE_DISTANCE,SAFE_RANGE['z']['MIN']))

def is_clear(z):
    return z >= SAFE_RANGE['z']['MIN'] + FEEDER_CLEARANCE

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    g = Gcode(f"{BUILD_DIR}/test.gcode")

    setup(g)
    
    for i, row in enumerate(MOSSAIC):
        for j, tile_index in enumerate(row):
            if not is_clear(g.get_z()):
                g.travel((0,0,FEEDER_CLEARANCE))
            g.travel_absolute((DESPENSER_COORD[0], DESPENSER_COORD[1],g.get_z()), feedrate=3000)
            despense_tile(g, tile_index)
            move_to_mossaic(g, i, j)

    end(g)
    
    # print the gcode to the console
    with open(f"{BUILD_DIR}/test.gcode", "r") as f:
        print(f.read())

    print("Done!")

if __name__ == "__main__":
    main()