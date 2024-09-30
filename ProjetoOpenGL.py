import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Definição dos vértices do cubo
verticies = (
    (2, -2, -2),
    (2, 2, -2),
    (-2, 2, -2),
    (-2, -2, -2),
    (2, -2, 2),
    (2, 2, 2),
    (-2, -2, 2),
    (-2, 2, 2)
)

# Definição das arestas do cubo
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
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Configuração de perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Mudar para matriz de modelagem
    glMatrixMode(GL_MODELVIEW)

    # Habilitar teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Cor de fundo preta
    glClearColor(0, 0, 0, 1)

    # Transladar o cubo para que ele seja visível
    initial_translation = [0.0, 0.0, -10.0]  # Posição inicial mais longe
    translation_x, translation_y, translation_z = 0.0, 0.0, 0.0

    # Variáveis para rotação e translação
    rotation_x, rotation_y = 0, 0
    mouse_down_left = False
    mouse_down_right = False
    last_mouse_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse para rotação
                    mouse_down_left = True
                    last_mouse_pos = pygame.mouse.get_pos()
                if event.button == 3:  # Botão direito do mouse para translação
                    mouse_down_right = True
                    last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Soltar botão esquerdo
                    mouse_down_left = False
                if event.button == 3:  # Soltar botão direito
                    mouse_down_right = False

            if event.type == pygame.MOUSEMOTION:
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                if mouse_down_left:
                    # Ajustar sensibilidade da rotação
                    sensitivity = 0.2
                    rotation_x += dy * sensitivity
                    rotation_y += dx * sensitivity

                if mouse_down_right:
                    # Ajustar sensibilidade da translação
                    translation_sensitivity = 0.01
                    translation_x += dx * translation_sensitivity
                    translation_y -= dy * translation_sensitivity  # Inverter eixo Y

                last_mouse_pos = current_mouse_pos

        # Limpar tela e buffer de profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Resetar matriz de modelagem
        glLoadIdentity()

        # Aplicar translação
        glTranslatef(translation_x + initial_translation[0],
                     translation_y + initial_translation[1],
                     initial_translation[2])

        # Aplicar rotação com base no movimento do mouse
        glRotatef(rotation_x, 1, 0, 0)  # Rotação no eixo X
        glRotatef(rotation_y, 0, 1, 0)  # Rotação no eixo Y

        Cube()

        pygame.display.flip()
        pygame.time.wait(10)

main()
