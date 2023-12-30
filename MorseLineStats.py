import matplotlib.pyplot as plt


def extractAllLenghts(raster_ml: list[bool]) -> None:
    """
    :param raster_ml:a 1D bool array which is result of ML pixel drop.
    :return: None
    """
    # go once over line, extract all length of series of falses and series of trues
    # (we can assume all lines begin with true)
    last_sign: bool = True
    blanks: list[int] = []
    signs: list[int] = []
    series_length_counter = 0
    for pos, value in enumerate(raster_ml):
        # If series end detected: append to stats
        if not last_sign == value:
            if not last_sign:
                signs.append(series_length_counter)
            else:
                blanks.append(series_length_counter)
            series_length_counter = 0
            last_sign = value
        else:
            series_length_counter += 1

    # return tuple with blanks and signs
    return blanks, signs
    # print("blanks: ")
    # print(blanks)
    # print("signs: ")
    # print(signs)


def visualize_distribution(samples: list[int], name: str):
    plt.hist(samples, bins=100)
    plt.title(name)
    plt.show()

def convert_to_ascii(blanks, signs):
    """
    we can assume every line begins with a space
    iterates blank and noted series and applies a thresholf of 10 pixels to distinguish between dots and scores / character spaces and word spaces.
    :param blanks:
    :param signs:
    :return:
    """
    result: str = ""
    threshold: int = 55
    for position in range(min(len(blanks), len(signs))):
        if blanks[position] <= threshold:
            result += ""
        else:
            result += " "
        if signs[position] <= threshold:
            result += "."
        else:
            result += "-"
    return result






