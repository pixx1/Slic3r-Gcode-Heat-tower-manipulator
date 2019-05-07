import os


input_file = "/home/jonas/3D_Druck/Kalibrieren/Temperature-Calibration_temp.gcode"
output_file = "/home/jonas/3D_Druck/Kalibrieren/Temperature-Calibration_temp_edit.gcode"

# Temperatures
maximum_temperature = 235
minimum_temperature = 190
steps_temperature = 5

# Layers
start_layer = 1
step_layer = 25

"""
Slic3r - Gcode Heat tower manipulator
 
Small script that manipulate the gcode for heat tower print.
I recommend to follow this documentation for preparing your slice:

https://github.com/slic3r/Slic3r/wiki/Calibration-of-Slic3r

You need to add this line in "After layer change G-Code
; Layer [layer_num]


    --------- Layer: 226 Temperature: 190 °C
    |       |
    |       |
    --------- Layer: 201 Temperature: 195°C
    |       |
   \/\/\/\/\/\/
    |       |
    --------- Layer: 26 Temperature: 230 °C
    |       |
    |       |
    --------- Layer: 1 Temperature: 235 °C


STL: https://www.thingiverse.com/thing:1548697
Doc: https://github.com/slic3r/Slic3r/wiki/Calibration-of-Slic3r

Misc:
If minimum temperature is reached all following layer will stay there. 
If output file exists, it will be removed. 
"""


def layer_and_temperature_generator() -> (int, int):
    """
    Generates layer number and temperature for new gcode file.
    If min temperature is reached but still layers left, it will stay at minimum temperature.
    :return: Layer and Temperature
    """

    layer = start_layer
    temperature = maximum_temperature

    while True:
        print(f"Layer {layer}, Temperature: {temperature}")
        yield layer, temperature
        layer += step_layer
        temperature -= steps_temperature

        if temperature < minimum_temperature:
            temperature = minimum_temperature


def write_line(file, content):
    with open(file, mode="a") as new_f:
        new_f.write(content)


def main(gcode_path, new_gcode_path):

    if os.path.isfile(output_file):
        os.remove(output_file)

    layer_stuff = layer_and_temperature_generator()
    layer_gen, temp_gen = next(layer_stuff)

    with open(gcode_path, "r") as file_content:

        for single_line in file_content:

            # catch stupid line in gcode
            if "; layer_gcode = ;" in single_line:
                continue

            # find line in code where layer information are
            if "; Layer" in single_line:
                layer_in_file = int(single_line[8:-1])

                if layer_in_file == layer_gen:
                    temperature_code = f"M104 T0 S{temp_gen}"
                    write_line(new_gcode_path, temperature_code)
                    layer_gen, temp_gen = next(layer_stuff)

            write_line(new_gcode_path, single_line)


if __name__ == '__main__':
    main(input_file, output_file)
