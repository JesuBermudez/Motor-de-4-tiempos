import pygame
import sys
import math

# Inicialización de Pygame
pygame.init()

# Tamaño de la pantalla
screen_width = 1080
screen_height = 720

# Creación de la ventana en modo ventana
screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar imagen de fondo
background_image = pygame.image.load("assets/fondo-cuerpo.png")

# Cargar imágenes de las partes del motor
cabeza_piston_image = pygame.image.load("assets/cabeza piston.png")
cuerpo_piston_image = pygame.image.load("assets/cuerpo piston.png")
ciguenal_image = pygame.image.load("assets/cigueñal.png")
tapa_frontal_image = pygame.image.load("assets/tapa frontal.png")
centro_rotatorio_image = pygame.image.load("assets/centro rotatorio.png")

# Tamaños de las imágenes
cabeza_piston_width, cabeza_piston_height = cabeza_piston_image.get_size()
cuerpo_piston_width, cuerpo_piston_height = cuerpo_piston_image.get_size()
ciguenal_width, ciguenal_height = ciguenal_image.get_size()

# Definir las coordenadas iniciales
cabeza_piston_x = 505
cabeza_piston_y = 280

cuerpo_piston_x = 503
cuerpo_piston_y = 328

ciguenal_x = 454
ciguenal_y = 435

# Ángulo de rotación inicial para el cigüeñal
ciguenal_angle = 0

ciguenal_center_x = ciguenal_x + (ciguenal_width / 2)
ciguenal_center_y = ciguenal_y + (ciguenal_height / 2)
centro_rotatorio_center_x = 514 + (67 / 2)
centro_rotatorio_center_y = 483 + (67 / 2)


# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el fondo
    screen.blit(background_image, (0, 0))

    # Dibujar las partes del motor
    rotated_ciguenal_image = pygame.transform.rotate(ciguenal_image, ciguenal_angle)
    rotated_centro_rotatorio_image = pygame.transform.rotate(centro_rotatorio_image, ciguenal_angle)

    # Calcular el centro
    cigueñal_centro = rotated_ciguenal_image.get_rect(center=(ciguenal_center_x, ciguenal_center_y))
    centro_rotatorio_centro = rotated_centro_rotatorio_image.get_rect(center=(centro_rotatorio_center_x, centro_rotatorio_center_y))

    # Calcular la posicion del pistón en y
    piston_y = ciguenal_center_y - (cuerpo_piston_width / 2) * (1 - math.cos(math.radians(ciguenal_angle + 180)))

    top_crank_y = ciguenal_center_y + 25 * math.cos(math.radians(ciguenal_angle - 180))
    top_crank_x = ciguenal_center_x + 25 * math.sin(math.radians(ciguenal_angle - 180))

    # Calcula el ángulo entre el punto de conexión de la cabeza del pistón y el punto de conexión del cigüeñal
    angle_degrees = math.degrees(math.atan2(top_crank_y - (cabeza_piston_y + cabeza_piston_height / 2), top_crank_x - (cabeza_piston_x + cabeza_piston_width / 2))) - 90


    # Rota la imagen del cuerpo del pistón según el ángulo calculado
    cuerpo_piston_image_rotated = pygame.transform.rotate(cuerpo_piston_image, -angle_degrees)

    
    # Dibuja las partes en sus posiciones
    screen.blit(cuerpo_piston_image_rotated, (top_crank_x - 3 - (cuerpo_piston_width / 2), piston_y - 90))
    screen.blit(cabeza_piston_image, (cabeza_piston_x, piston_y - 148))
    screen.blit(rotated_ciguenal_image, cigueñal_centro)
    screen.blit(tapa_frontal_image, (433, 518))
    screen.blit(rotated_centro_rotatorio_image, centro_rotatorio_centro)


    pygame.display.flip()

    ciguenal_angle += 1

    if ciguenal_angle >= 360:
        ciguenal_angle = 0  # Reinicia el ángulo


# Salir de Pygame
pygame.quit()
sys.exit()
