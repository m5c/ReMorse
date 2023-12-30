# This is a sample Python script.
import numpy as np
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from imageio.v2 import imread, imwrite
from numpy import ndarray, ubyte

from MorseLine import MorseLine
from MorseLineStats import extractAllLenghts, visualize_distribution, convert_to_ascii


def load_image() -> ndarray:
    """
    Loads image as numpy 2d array
    See library documentation: https://imageio.readthedocs.io/en/v2.9.0/userapi.html
    :return:
    """
    # Use a breakpoint in the code line below to debug your script.
    im: ndarray = imread("sample.png")
    return im


def rasterize_image(image: ndarray) -> list[list[bool]]:
    """
    Converts loaded ndarray image to all-or-nothing grid, where every cell is white (false) or 
    true (black).
    :return: 
    """
    raster_image: list[list[bool]] = []
    # iterate over image and for every line, rasterize.
    for line in image:
        raster_line: list[bool] = []
        for pixel in line:
            # TODO: actually interpret original pixel values here.
            # brightness is sum of rgb chanel. Divide by four in place to avoid overflow. Loss of
            # precision is not an issue.
            pixel_brightness: int = pixel[0] * 0.25 + pixel[1] * 0.25 + pixel[2] * 0.25
            raster_line.append(
                pixel_brightness > 100)  # This number is a magic value, needs to be adjusted per
            # image.
        raster_image.append(raster_line)
    return raster_image


def print_ascii_raster_image(raster_image: list[list[bool]]) -> None:
    """
    Prints an ascii representation of the received array
    :param raster_image:
    :return:
    """
    for line in raster_image:
        for position in line:
            if position:
                print(".", end='')
            else:
                print("x", end='')
        print("")
    return


def print_raster_image(ri: list[list[bool]], blank_lines: list[int], booster: int,
                       name: str) -> None:
    """
    converts a raster image back to ndarray that can be stored or displayed.
    :return: ndarray representation of image
    """
    # params are height, width, and 4 dimensions per pixel (rgb + alpha)
    im = np.ndarray(shape=(booster * len(ri), len(ri[0]), 4), dtype=ubyte)
    for lidx, line in enumerate(ri):
        for i in range(booster):
            for pidx, position in enumerate(line):
                pixel_value = 255 * int(position)
                im[lidx * booster + i][pidx][0] = pixel_value  # red (0-255)
                im[lidx * booster + i][pidx][1] = pixel_value  # green (0-255)
                im[lidx * booster + i][pidx][2] = pixel_value  # blue (0-255)
                im[lidx * booster + i][pidx][
                    3] = 255  # opacity (255 is opaque, 0 is transparent)

                # additionally, highlight all pixels in blank lines red:
                if lidx in blank_lines:
                    im[lidx * booster + i][pidx][1] = 0  # green
                    im[lidx * booster + i][pidx][2] = 0  # blue

    imwrite("~/Desktop/" + name + ".png", im, "png")


# Press the green button to run the script.
def is_blank(line: list[bool]):
    """
    Helper function that inspects if all raster pixels in a given line are blank (true / white)
    :param line:
    :return:
    """
    return


if __name__ == '__main__':
    # for i in range(10):
    #     print(i)

    # Load the file
    image: ndarray = load_image()

    # Convert to boolean raster grid
    raster_image: list[list[bool]] = rasterize_image(image)

    # The actual image processing starts here.
    # Detect blank lines
    blank_lines: list[int] = []
    for lidx, line in enumerate(raster_image):
        if all(line):
            blank_lines.append(lidx)
    # todo: chop by series of blank lines. create raster images for all lines.
    # print(blank_lines)

    # Just for fun, visualize the empty lines:
    print_raster_image(raster_image, blank_lines, 1, "blanks")

    # split image into morse lines, based on blank lines
    # iterate over all lines, every time a new block starts, carry over pixels to new morseline
    # object
    morse_lines: list[MorseLine] = []
    morse_line: MorseLine = MorseLine()
    previous_blank: bool = True
    for lidx, line in enumerate(raster_image):
        # on blank line: reset morse_line object, otherwise, append
        if lidx in blank_lines:
            # if this marks the end of a block: save the extracted morse line
            if not previous_blank:
                morse_lines.append(morse_line)
            morse_line: MorseLine = MorseLine()
            previous_blank = True
        else:
            morse_line.add_pixel_line(raster_image[lidx])
            previous_blank = False

    print("Lines detected: " + str(len(morse_lines)))

    # Apply pixel drop algorithm on every line detected
    raster_morse_lines: list[list[bool]] = []
    for morse_line in morse_lines:
        raster_morse_lines.append(morse_line.pixel_drop())

    # print the outcome. Visualizes the morse-code as 2d array
    print_raster_image(raster_morse_lines, [], 10, "drops")

    # print stats for all lines
    blanks = []
    signs = []
    for line in raster_morse_lines:
        result = extractAllLenghts(line)
        blanks.extend(result[0])
        signs.extend(result[1])
        print(convert_to_ascii(result[0], result[1]))
    visualize_distribution(blanks, "spaces")
    visualize_distribution(signs, "codes")
    # print(blanks)
    # print(signs)
