"""
GCODE info: https://marlinfw.org/meta/gcode/
"""
import os
from gcodepy.gcode import Gcode

# Constants
PUSHER_LENGTH = 24
PUSHER_WIDTH = 8
FEEDER_CLEARANCE = 30
PUSHER_TRAVEL_HIGHT = 10
FEEDER_WIDTH = 22.5
HOLE_DISTANCE = 16
TILE_SIZE = 10.6
TILE_SPACING = 2
PUSHER_CLEARANCE_Y = 94
X_MIN = -10
X_MAX = 190
Y_MIN = 9
Y_MAX = 215
Z_MIN = 34.5

# Adjust x and y as needed
DESPENSER_COORD = (186.6,193.6,Z_MIN)

BUILD_DIR = "build/"
MOSSAIC = [
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4]
]

def setup(gcode):
    # home print head skip z if already homed to save time
    gcode.file.write("G28 X Y\n")
    gcode.file.write("G28 O\n")
    gcode.file.write("M420 S1\n")

    # prepare the print head and give time to attach the pusher
    gcode.travel_absolute((141.8,Y_MAX,PUSHER_TRAVEL_HIGHT+Z_MIN))
    gcode.travel((X_MAX-gcode.get_x(),0,0))
    gcode.file.write("M0 S10 Press button to continue.\n")

def end(gcode):
    gcode.travel((0,0,FEEDER_CLEARANCE))
    gcode.close()

def despense_tile(gcode, tile_index):
    """
    Move x to the despenser side before using this function
    Moves the print head to the despenser and despenses a tile
    """
    gcode.travel_absolute((DESPENSER_COORD[0], DESPENSER_COORD[1]-tile_index*HOLE_DISTANCE, Z_MIN), feedrate=6000)
    gcode.travel((-PUSHER_LENGTH,0,0), feedrate=1000)
    gcode.travel((PUSHER_LENGTH,0,0), feedrate=1000)

    # prevent the tile from getting stuck
    gcode.travel((-PUSHER_LENGTH/2.9,0,0), feedrate=300)
    gcode.travel((PUSHER_LENGTH/2.9,0,0))

def move_to_mossaic(gcode, row, col):
    """
    Moves the print head to the mossaic and places the tile
    Run after despense_tile
    """
    # Move print head around feeder
    tile_location = (gcode.get_x()-(FEEDER_WIDTH+PUSHER_LENGTH),gcode.get_y()+PUSHER_WIDTH,PUSHER_TRAVEL_HIGHT+Z_MIN)
    gcode.travel_absolute((gcode.get_x(),PUSHER_CLEARANCE_Y,PUSHER_TRAVEL_HIGHT+Z_MIN), feedrate=6000)
    gcode.travel((-(PUSHER_LENGTH+FEEDER_WIDTH),0,0), feedrate=6000)
    gcode.travel_absolute(tile_location, feedrate=6000)
    gcode.travel((0,0,-PUSHER_TRAVEL_HIGHT))

    # Move tile to mossaic
    delta = TILE_SIZE + TILE_SPACING
    gcode.travel_absolute((X_MIN+col*delta, Y_MIN+row*delta, Z_MIN))

    # return to feeder
    gcode.travel((0,0,PUSHER_TRAVEL_HIGHT))
    gcode.travel_absolute((X_MAX,Y_MIN,PUSHER_TRAVEL_HIGHT+Z_MIN), feedrate=6000)

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    g = Gcode(f"{BUILD_DIR}/test.gcode")

    setup(g)
    
    for i, row in enumerate(MOSSAIC):
        for j, tile_index in enumerate(row):
            despense_tile(g, tile_index)
            move_to_mossaic(g, i, j)

    end(g)
    
    # print the gcode to the console
    with open(f"{BUILD_DIR}/test.gcode", "r") as f:
        print(f.read())

    print("Done!")

if __name__ == "__main__":
    main()