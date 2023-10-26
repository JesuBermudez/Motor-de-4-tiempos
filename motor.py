import pygame
import sys
from moviepy.editor import VideoFileClip
import math

pygame.init()

screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))

# Cargar imagen de fondo
background_image = pygame.image.load("assets/fondo-cuerpo.png")

# Cargar imágenes de las partes del motor
cabeza_piston_image = pygame.image.load("assets/cabeza piston.png")
cuerpo_piston_image = pygame.image.load("assets/cuerpo piston.png")
ciguenal_image = pygame.image.load("assets/cigueñal.png")
tapa_frontal_image = pygame.image.load("assets/tapa frontal.png")
centro_rotatorio_image = pygame.image.load("assets/centro rotatorio.png")

top_left_tube_image = pygame.image.load("assets/top left tube.png")
top_moving_left_image = pygame.image.load("assets/top moving left.png")
left_moving_image = pygame.image.load("assets/left moving.png")
valvula_admision_image = pygame.image.load("assets/valvula de admision.png")

top_right_tube_image = pygame.image.load("assets/top right tube.png")
top_moving_right_image = pygame.image.load("assets/top moving right.png")
right_moving_image = pygame.image.load("assets/right moving.png")
valvula_escape_image = pygame.image.load("assets/valvula de escape.png")

fix_bug = pygame.image.load("assets/fix bug.png")

gasolina_imagen = pygame.image.load("assets/gasolina.png")
humo_imagen = pygame.image.load("assets/humo.png")
explosion_imagen = pygame.image.load("assets/brillo.png")


# Tamaños de las imágenes
cabeza_piston_width, cabeza_piston_height = cabeza_piston_image.get_size()
cuerpo_piston_width, cuerpo_piston_height = cuerpo_piston_image.get_size()
ciguenal_width, ciguenal_height = ciguenal_image.get_size()

top_tube_width, top_tube_height = top_left_tube_image.get_size()
top_moving_width, top_moving_height = top_moving_left_image.get_size()
moving_width, moving_height = left_moving_image.get_size()

gasolina_width, gasolina_height = gasolina_imagen.get_size()
humo_width, humo_height = humo_imagen.get_size()


# Coordenadas iniciales
cabeza_piston_x = 505
cabeza_piston_y = 280

cuerpo_piston_x = 503
cuerpo_piston_y = 328

ciguenal_x = 454
ciguenal_y = 435

left_moving_y = 170
right_moving_y = 170

valvula_admision_y = 173
valvula_escape_y = 173

# Ángulo de rotación inicial
ciguenal_angle = 0

top_angle = 0

left_lever_angle = 0
right_lever_angle = 0

timer = 1

gasolina_opacity = 0
humo_opacity = 0
gasolina_scaled_height = 84
humo_scaled_height = 84

explosion_opacity = 0

ciguenal_center_x = ciguenal_x + (ciguenal_width / 2)
ciguenal_center_y = ciguenal_y + (ciguenal_height / 2)
centro_rotatorio_center_x = 514 + (67 / 2)
centro_rotatorio_center_y = 483 + (67 / 2)


clip = VideoFileClip("assets/init animation.mp4")
clip.preview()


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

    rotated_top_left_tube_image = pygame.transform.rotate(top_left_tube_image, top_angle)
    rotated_top_moving_left_image = pygame.transform.rotate(top_moving_left_image, top_angle)
    rotated_left_moving_image = pygame.transform.rotate(left_moving_image, left_lever_angle)

    rotated_top_right_tube_image = pygame.transform.rotate(top_right_tube_image, top_angle)
    rotated_top_moving_right_image = pygame.transform.rotate(top_moving_right_image, top_angle)
    rotated_right_moving_image = pygame.transform.rotate(right_moving_image, right_lever_angle)

    # Calcular el centro
    cigueñal_centro = rotated_ciguenal_image.get_rect(center=(ciguenal_center_x, ciguenal_center_y))
    centro_rotatorio_centro = rotated_centro_rotatorio_image.get_rect(center=(centro_rotatorio_center_x, centro_rotatorio_center_y))

    top_left_tube_centro = rotated_top_left_tube_image.get_rect(center=(479 + top_tube_width / 2, 148 + top_tube_height / 2))
    top_moving_left_centro = rotated_top_moving_left_image.get_rect(center=(470.5 + top_moving_width / 2, 141 + top_moving_height / 2))
    left_moving_centro = rotated_left_moving_image.get_rect(center=(475 + moving_width / 2, left_moving_y + moving_height / 2))
    
    top_right_tube_centro = rotated_top_right_tube_image.get_rect(center=(600 + top_tube_width / 2, 148 + top_tube_height / 2))
    top_moving_right_centro = rotated_top_moving_right_image.get_rect(center=(591 + top_moving_width / 2, 141 + top_moving_height / 2))
    right_moving_centro = rotated_right_moving_image.get_rect(center=(584 + moving_width / 2, right_moving_y + moving_height / 2))


    # Calcular la posicion del pistón en y
    piston_y = ciguenal_center_y - (cuerpo_piston_width / 2) * (1 - math.cos(math.radians(ciguenal_angle + 180)))

    top_crank_y = ciguenal_center_y + 25 * math.cos(math.radians(ciguenal_angle - 180))
    top_crank_x = ciguenal_center_x + 25 * math.sin(math.radians(ciguenal_angle - 180))

    # ángulo entre el punto de conexión de la cabeza del pistón y el punto de conexión del cigüeñal
    angle_degrees = math.degrees(math.atan2(top_crank_y - (cabeza_piston_y + cabeza_piston_height / 2), top_crank_x - (cabeza_piston_x + cabeza_piston_width / 2))) - 90

    cuerpo_piston_image_rotated = pygame.transform.rotate(cuerpo_piston_image, -angle_degrees)

    explosion_imagen.set_alpha(explosion_opacity)

    gasolina_imagen.set_alpha(gasolina_opacity)
    scaled_image = pygame.transform.scale(gasolina_imagen, (gasolina_width, gasolina_scaled_height))

    humo_imagen.set_alpha(humo_opacity)
    scaled_humo = pygame.transform.scale(humo_imagen, (humo_width, humo_scaled_height))

    
    # Partes en sus posiciones

    screen.blit(scaled_image, (cabeza_piston_x, cabeza_piston_y))
    screen.blit(scaled_humo, (cabeza_piston_x, cabeza_piston_y))
    

    screen.blit(cuerpo_piston_image_rotated, (top_crank_x - 3 - (cuerpo_piston_width / 2), piston_y - 90))
    screen.blit(cabeza_piston_image, (cabeza_piston_x, piston_y - 148))
    screen.blit(rotated_ciguenal_image, cigueñal_centro)
    screen.blit(tapa_frontal_image, (433, 518))
    screen.blit(rotated_centro_rotatorio_image, centro_rotatorio_centro)

    screen.blit(rotated_top_left_tube_image, top_left_tube_centro)
    screen.blit(rotated_top_moving_left_image, top_moving_left_centro)
    screen.blit(valvula_admision_image, (497, valvula_admision_y))
    screen.blit(rotated_left_moving_image, left_moving_centro)

    screen.blit(rotated_top_right_tube_image, top_right_tube_centro)
    screen.blit(rotated_top_moving_right_image, top_moving_right_centro)
    screen.blit(valvula_escape_image, (557, valvula_escape_y))
    screen.blit(rotated_right_moving_image, right_moving_centro)

    screen.blit(fix_bug, (0, 0))

    screen.blit(explosion_imagen, (0, 0))


    pygame.display.flip()


    top_angle += 0.5

    if top_angle >= 360:
        top_angle = 0

    ciguenal_angle += 1
    
    if ciguenal_angle >= 360:
        ciguenal_angle = 0


    if ciguenal_angle == 180:
        timer += 1
    
    if ciguenal_angle == 0 and timer == 3:
        timer = 1


    if timer == 1:
        if 0 <= ciguenal_angle < 120:
            left_lever_angle -= 0.2
            left_moving_y += 0.0666
            valvula_admision_y += 0.1083
            gasolina_opacity += 2.13
            if ciguenal_angle == 134:
                left_moving_y = 179
                valvula_admision_y = 186
        if 120 <= ciguenal_angle < 160:
            left_lever_angle += 0.6
            left_moving_y -= 0.2
            valvula_admision_y -= 0.325
            
    elif timer == 3:
        if 200 <= ciguenal_angle < 320:
            right_lever_angle += 0.2
            right_moving_y += 0.0666
            valvula_escape_y += 0.1083
            if ciguenal_angle == 314:
                right_moving_y = 179
                valvula_escape_y = 186
        if 320 <= ciguenal_angle < 360:
            right_lever_angle -= 0.6
            right_moving_y -= 0.2
            valvula_escape_y -= 0.325
            if ciguenal_angle == 350:
                humo_opacity = 0
                humo_scaled_height = 84

        if 180 <= ciguenal_angle < 360:
            humo_scaled_height -= 0.4666
        
    elif timer == 2:
        if 180 <= ciguenal_angle < 360:
            gasolina_scaled_height -= 0.4666

        if ciguenal_angle == 359:
            gasolina_opacity = 0
            gasolina_scaled_height = 84
        
        if 0 < ciguenal_angle < 16:
            explosion_opacity += 16
        elif 16 <= ciguenal_angle < 36:
            explosion_opacity -= 12.8

        if 0 <= ciguenal_angle < 120:
            humo_opacity += 2.13
            

    


# Salir de Pygame
pygame.quit()
sys.exit()
