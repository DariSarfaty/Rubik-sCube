# made by chatGPT
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Define a cubelet (unit cube with different colored faces)
def draw_colored_cube():
    vertices = [
        [1, 1,-1], [1,-1,-1], [-1,-1,-1], [-1, 1,-1],
        [1, 1, 1], [1,-1, 1], [-1,-1, 1], [-1, 1, 1]
    ]

    edges = (
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    )

    faces = (
        (0,1,2,3),  # back - blue
        (4,5,6,7),  # front - green
        (0,4,5,1),  # right - red
        (3,7,6,2),  # left - orange
        (0,4,7,3),  # top - white
        (1,5,6,2),  # bottom - yellow
    )

    colors = [
        (0, 0, 1),    # Blue
        (0, 1, 0),    # Green
        (1, 0, 0),    # Red
        (1, 0.5, 0),  # Orange
        (1, 1, 1),    # White
        (1, 1, 0)     # Yellow
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Create a 3x3x3 Rubik's Cube made of small cubes
def draw_rubiks_cube():
    offset = 2.01
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                glPushMatrix()
                glTranslatef(x * offset, y * offset, z * offset)
                draw_colored_cube()
                glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0]/display[1], 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -25)

    # Mouse rotation
    rot_x, rot_y = 20, 30
    mouse_down = False
    last_mouse_pos = (0, 0)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_mouse_pos = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == MOUSEMOTION:
                if mouse_down:
                    dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                    rot_x += dy * 0.5
                    rot_y += dx * 0.5
                    last_mouse_pos = event.pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -25)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        draw_rubiks_cube()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
