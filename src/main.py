'''
Universidad del Valle de Guatemala
Graficos por Computadora
Proyecto 2: Raycasting
Author: Javier Chavez
'''

import pygame
import math

class Vector2D:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __add__(self, v):
    return Vector2D(self.x + v.x, self.y + v.y)
  
  def __sub__(self, v):
    return Vector2D(self.x - v.x, self.y - v.y)
  
  def __mul__(self, k):
    return Vector2D(self.x * k, self.y * k)
  
  def copy(self):
    return Vector2D(self.x, self.y)
  
  def Magnitude(self):
    return math.hypot(self.x, self.y)
  
  def Sin(self):
    if self.Magnitude() == 0:
      return 0
    return self.y / self.Magnitude()
  
  def Cos(self):
    if self.Magnitude() == 0:
      return 0
    return self.x / self.Magnitude()
  
  def RotateInRads(self, angle):
    newAngle = self.GetAngleInRads() + angle
    magnitude = self.Magnitude()

    self.x = magnitude * math.cos(newAngle)
    self.y = magnitude * math.sin(newAngle)
  
  def GetAngleInRads(self):
    result = math.asin(self.Sin())
    if self.Cos() < 0:
      result = math.pi - result
    return result
  
  def SetAngleInRads(self, angle):
    magnitude = self.Magnitude()

    self.x = magnitude * math.cos(angle)
    self.y = magnitude * math.sin(angle)

class Player:
  def __init__(self, position, FOV, direction, movement_speed, rotation_speed):
    self.position = position
    self.FOV = FOV
    self.direction = direction
    self.movement_speed = movement_speed
    self.rotation_speed = rotation_speed

  def check_collision(self, proposed_position, map, cell_size):
    x_cell = int(proposed_position.x / cell_size)
    y_cell = int(proposed_position.y / cell_size)
    if map[y_cell][x_cell] == 1:
      return True
    return False
  
  def move_and_rotate(self, delta_time, keys, world_map, CELLSIZE):
    direction_vector = Vector2D(1, 0)
    direction_vector.SetAngleInRads(self.direction)

    if keys[pygame.K_w]:
      new_position_forward = Vector2D(self.position.x, self.position.y)
      new_position_forward += direction_vector * self.movement_speed * delta_time
      if not self.check_collision(new_position_forward, world_map, CELLSIZE):
        self.position = new_position_forward

    if keys[pygame.K_s]:
      new_position_forward = Vector2D(self.position.x, self.position.y)
      new_position_forward -= direction_vector * self.movement_speed * delta_time
      if not self.check_collision(new_position_forward, world_map, CELLSIZE):
        self.position = new_position_forward

    new_position = self.position.copy()

    if keys[pygame.K_w]:
      new_position += direction_vector * self.movement_speed * delta_time
      if not self.check_collision(new_position, world_map, CELLSIZE):
        self.position = new_position

    if keys[pygame.K_s]:
      new_position -= direction_vector * self.movement_speed * delta_time
      if not self.check_collision(new_position, world_map, CELLSIZE):
        self.position = new_position

    if keys[pygame.K_a]:
      self.direction -= self.rotation_speed * delta_time

    if keys[pygame.K_d]:
      self.direction += self.rotation_speed * delta_time

  def clamp_angle(self, angle):
    new_angle = 0
    if angle >= 0:
      new_angle = angle - angle // (2 * math.pi) * (2 * math.pi)
    else:
      pi2 = math.pi * 2
      new_angle = pi2 + ((abs(angle) // pi2) * pi2 + angle)
    return new_angle

  def cast_ray(self, direction, map, CELLSIZE, screen):
    angle = self.clamp_angle(direction)

    looks_up = not (0 < angle < math.pi)
    looks_right = not (math.pi / 2 < angle < 3 * math.pi / 2)

    ROV = 10

    tan = math.tan(direction)

    # Check horizontal intersection
    has_horizontal_intersection = False
    horizontal_distance = 0

    if tan != 0:
      # Projection of the vector to the nearest horizontal intersection
      yn = -(self.position.y - (self.position.y // CELLSIZE) * CELLSIZE)
      if not looks_up:
        yn = CELLSIZE + yn
      xn = yn / tan

      # Projection of the step vector
      ys = -CELLSIZE
      if not looks_up:
        ys = -ys
      xs = ys / tan

      current_x = self.position.x + xn
      current_y = self.position.y + yn
      for i in range(0, ROV + 1):
        ix = int(current_x // CELLSIZE)
        iy = int(current_y // CELLSIZE) - 1

        if not looks_up:
          iy += 1

        if ix < 0 or iy < 0 or ix > len(map[0]) - 1 or iy > len(map) - 1:
          break

        if map[iy][ix] == 1:
          has_horizontal_intersection = True
          horizontal_distance = (
            Vector2D(current_x, current_y) - self.position
          ).Magnitude()
          break

        current_x += xs
        current_y += ys

    # Check vertical intersection
    has_vertical_intersection = False
    vertical_distance = 0
    if tan != 1:
      # Projection of the vector to the nearest vertical intersection
      xn = -(self.position.x - (self.position.x // CELLSIZE) * CELLSIZE)
      if looks_right:
        xn = CELLSIZE + xn
      yn = tan * xn

      # Projection of the step vector
      xs = -CELLSIZE
      if looks_right:
        xs = -xs

      ys = tan * xs

      current_x = self.position.x + xn
      current_y = self.position.y + yn

      for i in range(0, ROV + 1):
        ix = int(current_x // CELLSIZE) - 1
        iy = int(current_y // CELLSIZE)

        if looks_right:
            ix += 1

        if ix < 0 or iy < 0 or ix > len(map[0]) - 1 or iy > len(map) - 1:
            break

        if map[iy][ix] == 1:
            has_vertical_intersection = True
            vertical_distance = (
              Vector2D(current_x, current_y) - self.position
            ).Magnitude()
            break

        current_x += xs
        current_y += ys

    distance = 0
    is_horizontal_the_nearest = False
    if has_horizontal_intersection and not has_vertical_intersection:
      distance = horizontal_distance
      is_horizontal_the_nearest = True
    elif has_vertical_intersection and not has_horizontal_intersection:
      distance = vertical_distance
    else:
      distance = min(horizontal_distance, vertical_distance)
      if horizontal_distance < vertical_distance:
        is_horizontal_the_nearest = True

    # Removing destortion
    beta = abs(self.clamp_angle(self.direction) - angle)
    if looks_up:
      beta = math.pi * 2 - abs(self.clamp_angle(self.direction) - angle)
    distance = distance * math.cos(beta)
    return (
      has_horizontal_intersection or has_vertical_intersection,
      distance,
      is_horizontal_the_nearest,
    )
  
# Functions

def draw_map(screen, map):
  wallColor = (60, 60, 60)
  floorColor = (115, 115, 115)
  cellSize = 35

  for y in range(0, len(map)):
    for x in range(0, len(map[0])):
      color = floorColor
      if map[y][x] == 1:
        color = wallColor

      current_x = x
      current_y = y
      pygame.draw.rect(
          screen,
          color,
          (
              current_x * cellSize,
              current_y * cellSize,
              current_x + cellSize,
              current_y + cellSize,
          ),
      )

def draw_player(screen, player, width, height, map_width, map_height):
    minimap_x = int(player.position.x / map_width * width)
    minimap_y = int(player.position.y / map_height * height)

    minimap_player_size = 4

    pygame.draw.circle(
      screen, (255, 255, 255), (minimap_x, minimap_y), minimap_player_size
    )
    pygame.draw.line(
      screen,
      (255, 255, 255),
      (minimap_x, minimap_y),
      (
        minimap_x + math.cos(player.direction) * minimap_player_size * 2,
        minimap_y + math.sin(player.direction) * minimap_player_size * 2,
      ),
    )

def render(screen, player, map, CELLSIZE, window_width, window_height, world_map):
    initial_color = (115, 115, 115)
    final_color = (80, 80, 80)
    half_cell = CELLSIZE / 2
    half_height = window_height / 2
    d = half_cell / math.tan(player.FOV / 2)

    current_angle = player.direction - player.FOV / 2
    step = player.FOV / (window_width - 1)
    for i in range(0, window_width):
        draw, length, draw_horizontal = player.cast_ray(
            current_angle, world_map, CELLSIZE, screen
        )
        h2 = (length / d) * half_cell
        if h2 != 0:
            line_ratio = half_cell / h2
            half_line_length = half_height * line_ratio
            if draw:
                color = final_color
                if draw_horizontal:
                    color = initial_color
                pygame.draw.line(
                    screen,
                    color,
                    (i, half_height + half_line_length),
                    (i, half_height - half_line_length),
                )
            current_angle += step

# Init map and its size
world_map = []

nivel1 = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
]

nivel2 = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

# Init window
window_width = int(320 * 2)
window_height = int(180 * 2.5)
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Proyecto 2: Raycasting")
pygame.font.init()
font = pygame.font.Font(None, int(window_height / 10))

# Main loop
fps = 1000
clock = pygame.time.Clock()
game_running = False
level1 = True
welcome_screen = True
selected_option = 0 
while welcome_screen:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      welcome_screen = False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    welcome_screen = False
    game_running = True

    if selected_option == 0:
      world_map = nivel1
    else:
      world_map = nivel2
  elif keys[pygame.K_q]:
    pygame.quit()

  if keys[pygame.K_w]:
    selected_option = 0  
  elif keys[pygame.K_s]:
    selected_option = 1 
    
  window.fill((0, 0, 0))

  welcome_font = pygame.font.Font(None, int(window_height / 15))
  welcome_text = welcome_font.render("Bienvenidos al juego", True, (255, 255, 255))
  option1_text = welcome_font.render("1. NIVEL 1", True, (255, 255, 255))
  option2_text = welcome_font.render("2. NIVEL 2", True, (255, 255, 255))
  controls_text = welcome_font.render("Presione Enter para jugar o Q para salir", True, (255, 255, 255))

  controls_text2 = welcome_font.render("WS para seleccionar nivel y moverse", True, (255, 255, 255))
  controls_text3 = welcome_font.render("AD para dirección", True, (255, 255, 255))

  welcome_rect = welcome_text.get_rect()
  option1_rect = option1_text.get_rect()
  option2_rect = option2_text.get_rect()
  controls_rect = controls_text.get_rect()

  welcome_rect.center = (window_width / 2, window_height / 4)
  option1_rect.center = (window_width / 2, window_height / 2.5)
  option2_rect.center = (window_width / 2, window_height / 2)
  controls_rect.center = (window_width / 2, window_height / 1.5)

  controls_rect2 = controls_text2.get_rect()
  controls_rect3 = controls_text3.get_rect()
  controls_rect2.center = (window_width / 2, window_height / 1.3)
  controls_rect3.center = (window_width / 2, window_height / 1.2)

  if selected_option == 0:
      option1_text = welcome_font.render("1. NIVEL 1", True, (0, 255, 0))
      option2_text = welcome_font.render("2. NIVEL 2", True, (255, 255, 255))
  else:
      option1_text = welcome_font.render("1. NIVEL 1", True, (255, 255, 255))
      option2_text = welcome_font.render("2. NIVEL 2", True, (0, 255, 0))

  window.blit(welcome_text, welcome_rect)
  window.blit(option1_text, option1_rect)
  window.blit(option2_text, option2_rect)
  window.blit(controls_text, controls_rect)
  window.blit(controls_text2, controls_rect2)
  window.blit(controls_text3, controls_rect3)

  pygame.display.update()

# Init size of map
CELLSIZE = 64
map_width = len(world_map[0]) * CELLSIZE
map_height = len(world_map) * CELLSIZE

# Init player
player_position = Vector2D(map_width / 2, map_height / 2)
player = Player(player_position, 80 * math.pi / 180, 0, 25, 3)

# Init game
run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  if game_running:
    delta_time = clock.tick(fps) / 1000

    window.fill((0, 0, 0))

    render(window, player, world_map, CELLSIZE, window_width, window_height, world_map)
    draw_map(window, world_map)
    draw_player(window, player, len(world_map) * 35, len(world_map[0]) * 35, map_width, map_height)

    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    text_rect = fps_text.get_rect()
    text_rect.topright = (window_width - 10, 10)
    window.blit(fps_text, text_rect)

    player.move_and_rotate(delta_time, pygame.key.get_pressed(), world_map, CELLSIZE)

    exit_font = pygame.font.Font(None, int(window_height / 15))
    exit_text = exit_font.render("Presione 'q' para salir", True, (255, 255, 255))
    exit_rect = exit_text.get_rect()
    exit_rect.bottomright = (window_width - 10, window_height - 10)
    window.blit(exit_text, exit_rect)

    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
      pygame.quit()
      game_running = False
      run = False

print("\n\n\n\t\t\t¡Gracias por explorar! :)\n\n\n")
