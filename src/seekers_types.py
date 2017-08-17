from hash_color import *

import random


class Vector:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y

  def __add__(left, right):
    return Vector(left.x+right.x, left.y+right.y)
  def __sub__(left, right):
    return Vector(left.x-right.x, left.y-right.y)
  def __neg__(self):
    return self*(-1)
  def __mul__(self, factor):
    return Vector(self.x*factor, self.y*factor)
  def __truediv__(self, divisor):
    return self * (1/divisor)
  def dot(self, other):
    return (self.x*other.x + self.y*other.y)

  def norm(self):
    return math.sqrt(self.x*self.x + self.y*self.y)
  def normalized(self):
    norm = self.norm()
    if (norm == 0):
      return Vector(0, 0)
    else:
      return Vector(self.x/norm, self.y/norm)

  def rotated(self):
    return Vector(-self.y, self.x)
      
  def fmap(self, f):
    return Vector(f(self.x),f(self.y))

class Goal:
  radius = 15

  def __init__(self, position):
    self.position = Vector(position.x, position.y)

class Seeker:
  radius = 20
  friction = 0.02
  max_speed = 5
  thrust = max_speed * friction
  disabled_time = 100

  def __init__(self, position, velocity=Vector(0, 0)):
    self.position = Vector(position.x, position.y)
    self.velocity = Vector(velocity.x, velocity.y)
    self.target = self.position
    self.disabled_counter = 0

  def disabled(self):
    return self.disabled_counter > 0

class ScoreAnimation:
  duration = 20

  def __init__(self, position, color):
    self.position = position
    self.age = 0
    self.color = color

class Player:
  win_score = 100

  def __init__(self, name):
    self.name = name
    self.color = string_hash_color(name)
    self.score = 0
    self.seekers = []

class World:
  def __init__(self, width, height):
    self.width = width
    self.height = height

  def normalize_position(self, pos):
    pos.x -= math.floor(pos.x/self.width)*self.width
    pos.y -= math.floor(pos.y/self.height)*self.height

  def size_vector(self):
    return Vector(self.width,self.height)

  def diameter(self):
    return self.size_vector().norm()

  def torus_distance(self,left,right):
    def dist1d(l,a,b):
      delta = abs(a-b)
      return min(delta,l-delta)
    return Vector( dist1d(self.width,right.x,left.x)
                 , dist1d(self.height,right.y,left.y) ).norm()

  def torus_direction(self,left,right):
    def dir1d(l,a,b):
      delta = abs(a-b)
      return b-a if delta < l-delta else a-b
    return Vector( dir1d(self.width,right.x,left.x)
                 , dir1d(self.height,right.y,left.y) ).normalized()


