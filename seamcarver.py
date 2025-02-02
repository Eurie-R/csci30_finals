#!/usr/bin/env python3

from picture import Picture
import math
import sys

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        """ 
        ^ For debugging purposes
        print (i, j)
        print(self.items())
        print(self.width(), self.height()) 
        """
        if not (0 <= i < self.width() and 0 <= j < self.height()):
            raise IndexError("Pixel indices out of range.")

        left = self[(i - 1) % self.width() if i > 0 else self.width() - 2, j]
        right = self[i % self.width() if i < self.width() else 0, j]
        up = self[i, (j - 1) % self.height() if j > 0 else self.height() - 2]
        down = self[i, j % self.height() if j < self.height() else 0]

        # Compute gradients for RGB components
        dx_r, dx_g, dx_b = (right[0] - left[0], right[1] - left[1], right[2] - left[2])
        dy_r, dy_g, dy_b = (down[0] - up[0], down[1] - up[1], down[2] - up[2])

        delta_x2 = dx_r**2 + dx_g**2 + dx_b**2
        delta_y2 = dy_r**2 + dy_g**2 + dy_b**2

        return math.sqrt(delta_x2 + delta_y2)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy vertical seam
        '''
        width, height = self.width(), self.height()
        energy_map = [[self.energy(i, j) for i in range(width)] for j in range(height)]
        dp = [[sys.maxsize] * width for _ in range(height)]
        path = [[0] * width for _ in range(height)]

        # Initialize the top row
        for i in range(width):
            dp[0][i] = energy_map[0][i]

        # Populate the DP table
        for j in range(1, height):
            for i in range(width):
                min_energy = dp[j - 1][i]
                if i > 0:
                    min_energy = min(min_energy, dp[j - 1][i - 1])
                if i < width - 1:
                    min_energy = min(min_energy, dp[j - 1][i + 1])

                dp[j][i] = energy_map[j][i] + min_energy

                # Track the path
                if min_energy == dp[j - 1][i]:
                    path[j][i] = i
                elif i > 0 and min_energy == dp[j - 1][i - 1]:
                    path[j][i] = i - 1
                else:
                    path[j][i] = i + 1

        # Backtrack to find the seam
        min_index = dp[-1].index(min(dp[-1]))
        seam = [0] * height
        for j in range(height - 1, -1, -1):
            seam[j] = min_index
            min_index = path[j][min_index]

        return seam

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy horizontal seam
        '''
        """ !! Non-functional implementation
        self.transpose_image()
        seam = self.find_vertical_seam()
        self.transpose_image()
        return seam
        """
        raise NotImplementedError

    """ !! Non-functional implementation
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
        self._width, self._height = self._height, self._width 
        """

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if len(seam) != self.height():
            raise SeamError("Invalid seam length.")
        if self.width() <= 1:
            raise SeamError("Cannot remove seam from image with width <= 1.")

        for j in range(self.height()):
            if j > 0 and abs(seam[j] - seam[j - 1]) > 1:
                raise SeamError("Invalid seam: adjacent entries differ by more than 1.")
            for i in range(seam[j], self.width() - 1):
                self[i, j] = self[i + 1, j]
            del self[self.width() - 1, j]

        self._width -= 1

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError


class SeamError(Exception):
    pass
