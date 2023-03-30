# Miles Waugh, 21/07/22
# Demo for rasterization with Python turtle.
# Uses backface culling, no depth-sorting.
# https://github.com/piano-miles/python-rasterizer

from turtle import *
from math import *

speed(0)
hideturtle()
screen = getscreen()
tracer(0, 0) # only refresh screen when update()
screen.bgcolor(50, 50, 50)

pi = 3.14159
ti = pi*2
hi = pi*0.5
sc = pi / 18

# light direction (user can change init values)
lx = -2
ly = 1
norm = sqrt(lx * lx + ly * ly)
lx /= norm
ly /= norm

xl = [] # geometry on x
yl = [] # geometry on y
one = [1]*37
neg = [-1]*37

for i in range(37): # precompute geometry
  xl.append(sin(i*sc))
  yl.append(cos(i*sc))

c = 1
s = 0
a = 0 # initialize rotation vars


def go(x, y, z): # move to projection
  w = 500/(c*z+s*x + 5)
  goto((c*x-s*z)*w, y*w)

def poly(x, y, z): # rasterize polygon
  for i in range(len(x)):
    go(x[i], y[i], z[i])
    if i == 0:
      begin_fill()
  end_fill()

def extrude(x, y): # render extrusion
  poly(x, y, [1, -1, -1, 1])


nz = 0
while True: # forever
  penup()
  clear() # init

  for i in range(36):
    nx = xl[i] # normals
    ny = yl[i]
    lam = max(nx*lx + ny*ly, 0) * 205 + 50 # lambert diffuse
    fillcolor(lam, lam*0.5, lam*0.2) # set face color
    nzr = s*nx # relative z-normal in camera space
    dot = nzr*(xl[i]*s + 5) # facing toward or away from camera
    if dot <= 0: # render extrusion if not culled
      extrude([xl[i], xl[i], xl[i+1], xl[i+1]],
              [yl[i], yl[i], yl[i+1], yl[i+1]])

  fillcolor(50, 25, 10)
  if (a+hi) % ti >= pi: # decide which cylinder cap to render
    if (c-s)/(s+c+5) < (-c-s)/(c-s+5): # cull correction for perspective
      poly(xl, yl, one) # back cap
  elif (c+s)/(s-c+5) > (s-c)/(-s-c+5):
    poly(xl, yl, neg) # front cap
  update() # update screen

  a += 0.02 # increment angle
  a %= ti
  s = sin(a) # precompute trig for rotation matrix
  c = cos(a)
