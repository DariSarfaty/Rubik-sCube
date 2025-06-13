import numpy as np


class Center:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f'{self.color}'


class Edge:
    def __init__(self, id, position, orientation):
        self.id = id # size 2 tuple
        self.position = id # initialize on same faces (solved)

    def __str__(self):
        return f'{self.id[0]} on the {self.position[0]} face and {self.id[1]} on the {self.position[1]} face'

    def is_solved(self):
        return self.position == self.id

class Corner:
    def __init__(self, id, position, orientation):
        self.id = id # size 3 tuple
        self.position = id # initialize on same faces (solved)
        self.orientation = 0 # 0 = normal ; 1 = cw rotated once ; 2 = cw rotated twice (or once ccw)

    def __str__(self):
        return f'{self.id[0]} on the {self.position[self.orientation]} face, {self.id[1]} on the {self.position[1 - self.orientation]} face and {self.id[2]} on the {self.position[2 - self.orientation]} face'

    def is_solved(self):
        return self.position == self.id
