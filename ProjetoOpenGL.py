import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Função para gerar vértices de um círculo
def generate_circle_vertices(radius, num_segments):
    vertices = []
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments  # Ângulo ao redor do círculo
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        vertices.append([x, y, 0])  # Coordenadas no plano XY, Z = 0
    return vertices

# Função para desenhar um círculo
def draw_circle(vertices):
    glBegin(GL_LINE_LOOP)
    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()

# Função para desenhar cilindro
def draw_cylinder(vertices_top, vertices_bottom):
    num_vertices = len(vertices_top)

    # Desenhar as tampas do cilindro (topo e fundo)
    glBegin(GL_LINE_LOOP)
    for vertex in vertices_top:
        glVertex3fv(vertex)
    glEnd()

    glBegin(GL_LINE_LOOP)
    for vertex in vertices_bottom:
        glVertex3fv(vertex)
    glEnd()

    # Desenhar as faces laterais conectando topo e fundo
    glBegin(GL_LINES)
    for i in range(num_vertices):
        glVertex3fv(vertices_top[i])
        glVertex3fv(vertices_bottom[i])
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

    # Definir propriedades do círculo
    radius = 2.0  # Raio do círculo
    num_segments = 32  # Número de segmentos (mais segmentos = círculo mais suave)

    # Gerar vértices do círculo
    circle_vertices = generate_circle_vertices(radius, num_segments)
    extrusion_height = 0.0  # Altura inicial da extrusão (círculo plano)

    # Transladar o círculo/cilindro para que ele seja visível
    initial_translation = [0.0, 0.0, -10.0]  # Para visualizar melhor
    translation_x, translation_y = 0.0, 0.0

    # Variáveis para rotação, translação e extrusão
    rotation_x, rotation_y = 0, 0
    mouse_down_left = False
    mouse_down_right = False
    last_mouse_pos = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Pressionar 'E' para extrusão
                    extrusion_height += 0.1  # Aumentar extrusão no eixo Z (transformar em cilindro)

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

        # Desenhar o círculo/cilindro com extrusão
        if extrusion_height == 0:
            draw_circle(circle_vertices)  # Desenhar apenas o círculo
        else:
            # Gerar vértices do topo e fundo do cilindro
            top_vertices = [[x, y, extrusion_height] for x, y, z in circle_vertices]  # Topo do cilindro
            bottom_vertices = circle_vertices  # Fundo do cilindro permanece no plano original
            draw_cylinder(top_vertices, bottom_vertices)  # Desenhar o cilindro

        pygame.display.flip()
        pygame.time.wait(10)

main()
