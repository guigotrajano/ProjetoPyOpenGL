import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
    [2, -2, -2],
    [2, 2, -2],
    [-2, 2, -2],
    [-2, -2, -2],
    [2, -2, 2],
    [2, 2, 2],
    [-2, -2, 2],
    [-2, 2, 2]
]

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:

            glColor3f(1.0, 0.3, 0.5)
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)


    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


    glEnable(GL_DEPTH_TEST)


    glClearColor(0, 0, 0, 1)


    initial_translation = [0.0, 0.0, -10.0]
    translation_x, translation_y = 0.0, 0.0
    rotation_x, rotation_y = 0, 0
    extrusion_z = 0.0
    scale_x, scale_y = 1.0, 1.0
    mouse_down_left, mouse_down_right = False, False
    last_mouse_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == VIDEORESIZE:

                screen = pygame.display.set_mode((event.w, event.h), DOUBLEBUF | OPENGL | RESIZABLE)


                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (event.w / event.h), 0.1, 50.0)
                glViewport(0, 0, event.w, event.h)
                glMatrixMode(GL_MODELVIEW)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    extrusion_z += 0.1
                    verticies[4][2] += extrusion_z
                    verticies[5][2] += extrusion_z
                    verticies[6][2] += extrusion_z
                    verticies[7][2] += extrusion_z

                if event.key == pygame.K_a:  # Pressionar 'A' para aumentar a escala
                    scale_x += 0.1
                    scale_y += 0.1

                if event.key == pygame.K_d:  # Pressionar 'D' para diminuir a escala
                    scale_x -= 0.1
                    scale_y -= 0.1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down_left = True
                    last_mouse_pos = pygame.mouse.get_pos()
                if event.button == 3:
                    mouse_down_right = True
                    last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down_left = False
                if event.button == 3:
                    mouse_down_right = False

            if event.type == pygame.MOUSEMOTION:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                if mouse_down_left:
                    sensitivity = 0.2
                    rotation_x += dy * sensitivity
                    rotation_y += dx * sensitivity

                if mouse_down_right:
                    translation_sensitivity = 0.01
                    translation_x += dx * translation_sensitivity
                    translation_y -= dy * translation_sensitivity

                last_mouse_pos = current_mouse_pos


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        glLoadIdentity()


        glTranslatef(translation_x + initial_translation[0],
                     translation_y + initial_translation[1],
                     initial_translation[2])


        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)


        glScalef(scale_x, scale_y, 1.0)

        Cube()

        pygame.display.flip()
        pygame.time.wait(10)

main()
