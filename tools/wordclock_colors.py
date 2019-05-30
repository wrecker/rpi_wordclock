import math

try:
    from rpi_ws281x import Color
except:
    from GTKstrip import Color

# Define colors which are available for the wcd. Currently: Alphabetic order
BLACK = Color(  0,  0,  0)
BLUE  = Color(  0,  0,255)
GREEN = Color(  0,255,  0)
PINK  = Color(255,  0,170)
RED   = Color(255,  0,  0)
WHITE = Color(255,255,255)
WWHITE= Color(255,255, 50)  # Warm white
YELLOW= Color(255,255,  0)
ORANGE= Color(212,165,  25)

# Summarize colors: [BLACK->WHITE, RED->BLUE (rainbow)]
colors = [BLACK, WHITE, WWHITE, RED, YELLOW, GREEN, BLUE]
num_of_colors = len(colors)


def color_temperature_to_rgb(color_temperature):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/

    Implementation courtesy of
    https://gist.github.com/petrklus/b1f427accdf7438606a6
    """
    # range check
    if color_temperature < 1000:
        color_temperature = 1000
    elif color_temperature > 40000:
        color_temperature = 40000

    tmp_internal = color_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red

    # green
    if tmp_internal <= 66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green

    # blue
    if tmp_internal >= 66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue

    return Color(int(red), int(green), int(blue))
