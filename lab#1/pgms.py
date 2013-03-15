import os, sys, math, pygame, pygame.mixer
from pygame.locals import *
from euler import *
from time import sleep
import matplotlib.pyplot as plt
import pygbutton

LIGHTGRAY = pygbutton.LIGHTGRAY
GRAY = (120, 120, 120)

h = 1.0/60
START = 0.0
END = 60.0

m = float(raw_input("Mass of the object:     "))
c = float(raw_input("Constant of the spring: "))
k = float(raw_input("Constant of the damper: "))
sel = raw_input("Select function [1, 2, 3]: ")

if sel == '1':
  x, y = euler_sdm(h, START, END, m, c, k, func_sin_cos_st)
elif sel == '2':
  x, y = euler_sdm(h, START, END, m, c, k, func_sin_cos_inst)
elif sel == '3':
  x, y = euler_sdm(h, START, END, m, c, k, func_zero)

plt.plot(x, y)
plt.ion()
plt.show()

# Defining the screen size
screen_size = screen_width, screen_height = 320, 600

# Defining the display
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)

# Getting the clock object
clock = pygame.time.Clock()

# Setting the title of the window
pygame.display.set_caption("Spring-Damper-Mass simulation")

class MassCircleSpring:
  def __init__(self, (x, y), size, color = (0, 0, 0), width = 1):
    self.index = 0
    self.x = x
    self.y = y
    self.size = size
    self.color = color
    self.width = width
    self.norm = 0
    self.mult = 1
    self.offset = screen_height
    self.normalize()
    self.running = False
    self.metal = True


  def normalize(self):
    # Getting the minimal element from the list
    self.norm = min(self.y)
    # Inversing the sign of the minimal elm
    self.norm *= -1

    # Computing the multiplier
    self.mult = (self.offset-self.size*4) / (max(y) + self.norm)


  def get_y(self):
    if self.index >= len(self.y):
      self.index = 0

    val = self.y[self.index] + self.norm
    val *= self.mult
    val = self.offset - self.size*2 - val

    self.index += 1
    return int(val)


  def display(self):
    if not self.running and self.index:
      self.index -= 1

    ty = self.get_y()
    if self.metal:
      start_ball_y = ty - self.size
      coils = 60
      points = ()
      item = (self.x, start_ball_y)
      points = (item, ) + points
      item = (self.x, start_ball_y - 10)
      points = (item, ) + points
      tmp = start_ball_y - 10
      incrementer = (start_ball_y) / float(coils)
      for i in reversed( range(coils + 10) ):
        if i%2:
          item = (self.x + 25, tmp)
        else:
          item = (self.x - 25, tmp)
        points = (item,) + points
        tmp -= incrementer

      pygame.draw.aalines(screen, (0,0,0), False, points, 4)
    else:
      thickness = self.offset - ty
      thickness /= 10
      thickness += 1
      pygame.draw.line(screen, (0, 0, 255), (self.x, 0), (self.x, ty), thickness)

    pygame.draw.circle(screen, self.color, (self.x, ty), self.size, self.width)


  def reset(self):
    self.index = 0
    self.running = True


  def pause(self):
    if self.running:
      self.running = False
    else:
      self.running = True


  def spring(self, choice):
    if choice == 'metal':
      self.metal = True
    else:
      self.metal = False

spring_object = MassCircleSpring((50, y), 30, (90, 90, 90), 0)

restart_btn = pygbutton.PygButton((210, 10, 100, 30), 'Restart')
pause_btn = pygbutton.PygButton((100, 10, 100, 30), 'Play / Pause')

metal_btn = pygbutton.PygButton((100, 50, 100, 30), 'Metal spring', bgcolor=GRAY)
rubber_btn = pygbutton.PygButton((210, 50, 100, 30), 'Rubber')

max_fps = 60
running = True

while running:
  # Limiting the framerate
  clock.tick(max_fps)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if 'click' in restart_btn.handleEvent(event):
      spring_object.reset()
    if 'click' in pause_btn.handleEvent(event):
      spring_object.pause()
    if 'click' in rubber_btn.handleEvent(event):
      spring_object.spring('rubber')
      rubber_btn.bgcolor = GRAY
      metal_btn.bgcolor = LIGHTGRAY
    if 'click' in metal_btn.handleEvent(event):
      spring_object.spring('metal')
      rubber_btn.bgcolor = LIGHTGRAY
      metal_btn.bgcolor = GRAY
  # Screen filling with white
  screen.fill((255, 255, 255))

  spring_object.display()
  restart_btn.draw(screen)
  pause_btn.draw(screen)
  metal_btn.draw(screen)
  rubber_btn.draw(screen)
  # Displaying all the content
  pygame.display.flip()

pygame.quit()
sys.exit()
