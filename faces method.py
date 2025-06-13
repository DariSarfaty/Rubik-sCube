import numpy as np
import copy

class Face:
    def __init__(self, color):
        self.color = color
        self.array = np.full((3,3), color)  # initialize as center color
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.across = 0

    def is_solved(self):
        return self.array == np.full((3,3), self.color)

    def rotate(self, ccw):  # ccw = 1, cw = -1
        self.array = np.rot90(self.array, ccw)

    def swap(self, array, side):
        if side == self.left:
            self.array[:, 0] = np.flip(array)
        elif side == self.right:
            self.array[:, 2] = array
        elif side == self.up:
            self.array[0, :] = array
        elif side == self.down:
            self.array[2, :] = np.flip(array)
        else:
            raise NotImplementedError

    def relatives(self, others):
        self.left = others[0]
        self.right = others[2]
        self.up = others[1]
        self.down = others[3]
        self.across = others[4]

    def adjacent(self):
        return [self.left, self.up, self.right, self.down]

    def side(self, other):
        if other == self.left:
            return np.flip(self.array[:, 0].copy())
        elif other == self.right:
            return self.array[:, 2].copy()
        elif other == self.up:
            return self.array[0, :].copy()
        elif other == self.down:
            return np.flip(self.array[2, :].copy())
        else:
            raise NotImplementedError

    def __str__(self):
        return f'{self.color} face:\n{self.up.color}\n{self.left.color}{self.array}{self.right.color}\n{self.down.color}\n'

class Cube:
    def __init__(self):
        self.white = Face('W')
        self.yellow = Face('Y')
        self.green = Face('G')
        self.red = Face('R')
        self.blue = Face('B')
        self.orange = Face('O')
        self.faces = [self.white, self.red, self.blue, self.yellow, self.orange, self.green]
        self.white.relatives([self.red, self.green, self.orange, self.blue, self.yellow])
        self.blue.relatives([self.red, self.white, self.orange, self.yellow, self.green])
        self.green.relatives([self.orange, self.white, self.red, self.yellow, self.blue])
        self.red.relatives([self.green, self.white, self.blue, self.yellow, self.orange])
        self.orange.relatives([self.blue, self.white, self.green, self.yellow, self.red])
        self.yellow.relatives([self.red, self.blue, self.orange, self.green, self.white])

    def rotate(self, face, ccw):
        face.rotate(ccw)
        adj_array = face.adjacent()
        edges = [x.side(face) for x in adj_array]
        if ccw == 1:
            orders = [ 1, 2, 3, 0]
        else:
            orders = [3, 0, 1, 2]
        reordered = [edges[i] for i in orders]
        for i, s in enumerate(adj_array):
            s.swap(reordered[i], face)

    def __repr__(self):
        string = ''
        for face in self.faces:
            string += str(face)
        return string

cube = Cube()
cube.rotate(cube.blue, -1)
cube.rotate(cube.white, 1)
cube.rotate(cube.red, -1)
cube.rotate(cube.blue, 1)
cube.rotate(cube.yellow, -1)
cube.rotate(cube.orange, 1)
cube.rotate(cube.green, 1)
cube.rotate(cube.white, -1)
print(cube)