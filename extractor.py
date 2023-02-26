import colorgram
import ttkbootstrap.colorutils as tcl


def get_colour(file_path: str, number_of_colours: int) -> list:
    """
    This function takes an image file path and a number of colours to be
    extracted from the image file and returns a list of dictionaries
    with rgb, hsl and hex as keys and its corresponding values
    """
    colour_list = []

    extract = colorgram.extract(file_path, number_of_colours)

    rgb_colours = [i.rgb for i in extract]
    hsl_colours = [i.hsl for i in extract]

    for a, b in zip(rgb_colours, hsl_colours):
        colour_list.append(
            {
                "rgb": (a.r, a.g, a.b),
                "hsl": (b.h, b.s, b.l),
                "hex": tcl.color_to_hex(a, model='rgb')
            }
        )
    return colour_list


