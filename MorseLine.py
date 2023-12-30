class MorseLine:
    """
    represents morse line, that is a 2D array with boolean values.
    """

    def __init__(self):
        self.__raster_line: list[list[bool]] = []


    def pixel_drop(self) -> list[bool]:
        """
        Classic pixel drop implementation. Checks if any pixel in current collumn is false, and if yes sets target pixel to false.
        :return:
        """
        target_pixel_line: list[bool] = []
        for cidx, whatever in enumerate(self.__raster_line[0]):
            # iterate over all pixels in column and set to false if at least one pixel is false
            column_pixels: list[bool] = [row[cidx] for row in self.__raster_line]
            target_pixel_line.append(all(column_pixels))
        print(target_pixel_line)
        return target_pixel_line

    def add_pixel_line(self, pixel_line: list[bool]) -> None:
        self.__raster_line.append(pixel_line)


