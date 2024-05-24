import os
from gcodepy.gcode import Gcode

build_dir = "build/"

def rotate_gear(gcode, rate, amount):
    if rate < 0:
        raise ValueError("Rate must be positive")
    gcode.file.write(f"G1 F{rate} E{amount}\n")

def setup(gcode):
    gcode.file.write("G28 X Y\n") # home x and y
    gcode.file.write("M302 S0\n") # allow extrusion without heating

def square_test(gcode):
    gcode.travel_absolute((0,0,0))
    gcode.travel_absolute((200,0,20))
    gcode.travel_absolute((200,200,30))
    gcode.travel_absolute((0,200,20))
    rotate_gear(gcode, 70, -20)
    gcode.travel_absolute((0,0,0))

def main():
    os.makedirs(build_dir, exist_ok=True)
    g = Gcode(f"{build_dir}/test.gcode")

    setup(g)
    square_test(g)
    g.close()
    
    with open(f"{build_dir}/test.gcode", "r") as f:
        print(f.read())

    print("Done!")

if __name__ == "__main__":
    main()