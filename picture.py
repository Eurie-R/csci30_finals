#!/usr/bin/env python3

from PIL import Image
from PyQt6.QtGui import QImage, QPixmap

class Picture(dict):
    def __init__(self, img: Image.Image):
        '''
        Take a PIL image, and store pixels in its dictionary
        '''
        self._width, self._height = img.size
        pixels = iter(img.getdata())
        for j in range(self._height):
            for i in range(self._width):
                self[i, j] = next(pixels)

    """ !! Currently non-functional
    def transpose_image(self): 
        '''
        Transpose the image (swap width and height)
        '''
        # Create a 2D representation of the image
        grid = [[self[i, j] for j in range(self._height)] for i in range(self._width)]
        
        # Transpose using a list comprehension
        transposed_grid = list(zip(*grid))
        
        # Rebuild the pixel dictionary from the transposed grid
        self._pixels = {(x, y): transposed_grid[x][y] for x in range(len(transposed_grid)) for y in range(len(transposed_grid[0]))}
        
        # Update dimensions
        self._width = self._height
        self._height = self._width """

    def picture(self) -> Image.Image:
        '''
        Get the current picture represented by self
        '''
        picture = Image.new('RGB', (self._width, self._height))
        # print(f'w: {self._width} h: {self._height}')
        picture.putdata([self[i, j] for j in range(self._height) for i in range(self._width)])
        return picture

    def width(self) -> int:
        '''
        Return the width of current picture
        '''
        return self._width

    def height(self) -> int:
        '''
        Return the height of current picture
        '''
        return self._height

    def show(self):
        '''
        Open the current picture using the default image viewer
        '''
        self.picture().show()

    def color_seam(self, seam: list[int], vertical=True, color: tuple =(255, 0, 255)):
        '''
        Color a seam in the current picture with the specified color
        '''
        for i, j in enumerate(seam):
            if vertical:
                self[j, i] = color
            else:
                self[i, j] = color

    def _to_pixmap(self) -> QPixmap:
        '''
        (Internal use only) Convert the current picture into a QPixmap object for the GUI display
        '''
        img = self.picture()
        data = img.tobytes('raw', 'RGB')
        stride = len(data)//self._height
        qim = QImage(data, self._width, self._height, stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qim)
