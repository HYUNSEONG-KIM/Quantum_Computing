from tkinter import colorchooser

def interpolate_color(color1, color2, factor: float) -> str:
    """
    Interpolates between two colors in the RGB space.

    :param color1: The starting color in the '#RRGGBB' format.
    :param color2: The ending color in the '#RRGGBB' format.
    :param factor: A value between 0 and 1 that indicates the interpolation factor.
                   0 will return color1, 1 will return color2.
    :return: The interpolated color in the '#RRGGBB' format.
    """
    if factor < 0 or factor > 1:
        factor =0 if factor <0 else 1

    r1, g1, b1 = color1[1:3], color1[3:5], color1[5:7]
    r2, g2, b2 = color2[1:3], color2[3:5], color2[5:7]

    r1, g1, b1 = int(r1, 16), int(g1, 16), int(b1, 16)
    r2, g2, b2 = int(r2, 16), int(g2, 16), int(b2, 16)

    r = round(r1 + (r2 - r1) * factor)
    g = round(g1 + (g2 - g1) * factor)
    b = round(b1 + (b2 - b1) * factor)

    return f'#{r:02x}{g:02x}{b:02x}'

def color_function(value: float) -> str:
    """
    Maps a real number in the range [0, 1] to a color between pink1 and cyan.

    :param value: A real number between 0 and 1.
    :return: The corresponding color in the '#RRGGBB' format.
    """
    return interpolate_color('#ffb6c1', '#00ffff', value)

