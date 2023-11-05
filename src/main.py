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
