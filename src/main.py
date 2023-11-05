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

