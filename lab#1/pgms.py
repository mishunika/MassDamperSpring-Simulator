import os, sys, math, pygame, pygame.mixer
from pygame.locals import *
from euler import *
from time import sleep
import matplotlib.pyplot as plt

h = 1.0/60
START = 0.0
END = 60.0

m = 10.0
c = 15.0
k = 100.0

x, y = euler_sdm(h, START, END, m, c, k, func_sin_cos_inst)
plt.plot(x, y)
plt.ion()
plt.show()

# Defining the screen size
screen_size = screen_width, screen_height = 800, 600

# Defining the display
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)

# Getting the clock object
clock = pygame.time.Clock()

# Setting the title of the window
pygame.display.set_caption("Spring-Damper-Mass simulation")

class MassCircle:
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

    val = y[self.index] + self.norm
    val *= self.mult
    val = self.offset - self.size*2 - val

    self.index += 1
    return int(val)


  def display(self):
    ty = self.get_y()
    thickness = self.offset - ty
    thickness /= 20
    thickness += 1
    pygame.draw.line(screen, (0,0,0), (self.x, 0), (self.x, ty), thickness)
    pygame.draw.circle(screen, self.color, (self.x, ty), self.size, self.width)

circle = MassCircle((300, y), 30, (90, 90, 90), 0)

max_fps = 60
running = True

while running:
  # Limiting the framerate
  clock.tick(max_fps)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Screen filling with white
  screen.fill((255, 255, 255))

  circle.display()
  # Displaying all the content
  pygame.display.flip()

pygame.quit()
sys.exit()
