import numpy as np
import itertools

class Face:
    def __init__(self, color):
        self.color = color
        self.array = np.full((3,3), color)  # initialize as center color
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.across = 0

    def all_edges_on_face(self, color):
        my_array = []
        if self.array[1, 0] == color:
            my_array.append(self.left)
        if self.array[0, 1] == color:
            my_array.append(self.up)
        if self.array[1, 2] == color:
            my_array.append(self.right)
        if self.array[2, 1] == color:
            my_array.append(self.down)
        return my_array

    def all_corners_on_face(self, color):
        my_array = []
        if self.array[0, 0] == color:
            my_array.append((self.left, self.up))
        if self.array[0, 2] == color:
            my_array.append((self.up, self.right))
        if self.array[2, 2] == color:
            my_array.append((self.right, self.down))
        if self.array[2, 0] == color:
            my_array.append((self.down, self.left))
        return my_array

    def corner_color(self, others):
        others = set(others)
        if {self.left, self.up} == others:
            return self.array[0,0]
        elif {self.up, self.right} == others:
            return self.array[0,2]
        elif {self.right, self.down} == others:
            return self.array[2,2]
        elif {self.left, self.down} == others:
            return self.array[2,0]
        else:
            raise NotImplementedError

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

    def side(self, other):  # returns the edges on other's side
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

    def find_edge(self, colors):
        for primary in self.faces:
            for secondary in primary.all_edges_on_face(colors[0]):
                if primary in secondary.all_edges_on_face(colors[1]):
                    return primary, secondary
        raise Exception('No edge found')

    def find_corner(self, colors):
        for perm in itertools.permutations(colors):
            color1, color2, color3 = perm
        for primary in self.faces:
            print(primary.color)
            for face1, face2 in primary.is_corner_on_face(color1):
                print(face1.color, face2.color)
                for tup1 in face1.is_corner_on_face(color2):
                    if {face2, primary} == set(tup1):
                        for tup2 in face2.is_corner_on_face(color3):
                            if {face1, primary} == set(tup2):
                                return primary, face1, face2  # returns in "random" order cause of permutations
        raise Exception('No corner found')

    def find_corner_8(self, colors):
        pos = []
        my_set = set(colors)
        faces1 = self.white.adjacent()
        faces2 = [faces1[3], faces1[0], faces1[1], faces1[2]]
        whites = [self.white for _ in range(4)]
        yellows = [self.yellow for _ in range(4)]
        for white, primary, secondary in zip(whites, faces1, faces2):
            if {white.corner_color([primary,secondary]), primary.corner_color([white, secondary]), secondary.corner_color([white, primary])} == my_set:
                pos = [white, primary, secondary]
        for yellow, primary, secondary in zip(yellows, faces1, faces2):
            if {yellow.corner_color([primary, secondary]), primary.corner_color([yellow, secondary]),secondary.corner_color([yellow, primary])} == my_set:
                pos = [yellow, primary, secondary]
        first, second, third = pos
        my_array = [first.corner_color([second, third]), second.corner_color([first, third]), third.corner_color([first, second])]
        color_to_face = dict(zip(my_array, pos))  # map color from corner_color to the originating face
        reordered = [color_to_face[c] for c in colors]
        return reordered

    def __repr__(self):
        string = ''
        for face in self.faces:
            string += str(face)
        return string

if __name__ == '__main__':
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
    co = ['W', 'B', 'O']
    print("finding the following corner:", co)
    a = cube.find_corner_8(co)
    print("found corner on following edges:", a[0].color,a[1].color,a[2].color)

