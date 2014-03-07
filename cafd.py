#! /usr/bin/env python

import pygame
import simple3d
import sys
import view3d

from math import floor

def makeRGB(r,g,b) :
   return (floor(r*255),floor(g*255),floor(b*255))

debug = False

# window dimensions
w = 600
h = 600
# slightly off-white background
bgcolor = (0xf5,0xf5,0xf5)
# CPU throttle (larger value ==> less CPU hogging)
delay = 200
# key repeat delay, interval
key_delay = 20
key_interval = 20
# radians per key press for rotations
theta = 0.025   # 4.5 degrees
# displacement per key press for i, o
incr = 0.05

fish = simple3d.Simple3d()
#fish.load_object("objects", "tst2")

if len(sys.argv) < 2 :
   print( "usage: cafd.py object" )
   print( "where object names a set of files in the objects subfolder," )
   print( "to wit:" )
   print( "objects/object.faces" )
   print( "objects/object.edges" )
   print( "objects/object.vertices" )
   exit()
   
wireframe = True
erase = True

fish.load_object("objects", sys.argv[1])
eye = (0.0, 0.0, -5.0)
fish.set_eye(eye)
# screen (l,t,r,b), viewport (l,t,r,b), world "frustum" (really a box), eye (x,y,z), distance from eye to screen
view = view3d.View3d((0,0, w,h), (-1.0,-1.0, 1.0,1.0), (-1.0, 1.0, -1.0, 1.0, -1.0, 1.0), eye, 1.0)

if debug :
   fish.debug()
   view.debug()

# using +1 here to avoid using -1 elsewhere
screen = pygame.display.set_mode((w+1, h+1))
clock = pygame.time.Clock()
pygame.key.set_repeat(key_delay, key_interval)
running = True
sort_mode = "min"

while running:
   for event in pygame.event.get() :
      if event.type == pygame.QUIT :
         running = False
      elif event.type == pygame.KEYUP :
         # current list of recognized keys: b,c,d,e,h,i,l,o,q,r,s,u,w,x,y,z (and the 4 arrows)
         # current list of differenti8d capitals: C,X,Y,Z
         if event.key == pygame.K_b :
            fish.assign_random_blue_colors()
         elif event.key == pygame.K_c :
            if current_unicode == "C" :
               fish.assign_random_dark_colors()
            else :
               fish.assign_random_colors()           
         elif event.key == pygame.K_d :
            # debug the object
            fish.debug()
         elif event.key == pygame.K_e :
            # toggle bg erase
            erase = not erase
         elif event.key == pygame.K_h :
            print( '===============================================================================' )
            print( '         b: colorize (replace all edge & face colors with random "blue" colors)' )
            print( '         c: colorize (replace all edge & face colors with random colors)' )
            print( '         C: colorize (replace all edge & face colors with random "dark" colors)' )
            print( '         d: debug' )
            print( '         e: toggle erase-between-frames' )
            print( '      h(H): print this help info' )
            print( '         i: (in) move object toward viewer ( -z )' )
            print( '         l: (re)load object (restore original orientation & colors)' )
            print( '         o: (out) move object away from viewer ( +z )' )
            print( '         q: quit' )
            print( '         r: record object to file (appends "-new" to original name)' )
            print( '         s: change z-sort mode (min, max, avg)' )
            print( '         u: un-colorize (show monochrome pseudo-shaded)' )
            print( '         v: vectorize (record object to .svg file representation)' )
            print( '         w: toggle between wireframe & "solid" representation' )
            print( '      x(X): rotate cw(CCW) about the x axis' )
            print( '      y(Y): rotate cw(CCW) about the y axis' )
            print( '      z(Z): rotate cw(CCW) about the z axis' )
            print( 'arrow keys: move object left, right, up, down ( -x, +x, +y, -y )' )
            print( '===============================================================================' )
         elif event.key == pygame.K_l :
            # reload the object
            fish = simple3d.Simple3d()
            fish.load_object("objects", sys.argv[1])
         elif event.key == pygame.K_r :
            # record the object
            fish.store_object("objects", sys.argv[1] + "-new")
         elif event.key == pygame.K_s :
            # change sort mode
            if sort_mode == "min" :
               sort_mode = "max"
            elif sort_mode == "max" :
               sort_mode = "avg"
            else :
               sort_mode = "min"
            print( "sort_mode = %s" % sort_mode )
         elif event.key == pygame.K_u :
            wireframe = False
            fish.assign_grey_shade()
         elif event.key == pygame.K_v :
            # record the object
            fish.store_object("objects", sys.argv[1] + "-svg")
         elif event.key == pygame.K_w :
            # toggle wireframe
            wireframe = not wireframe
      elif event.type == pygame.KEYDOWN :
         current_unicode = event.unicode
         if event.key == pygame.K_i :
            # zoom in
            view.distance += incr
            if debug : print( view.distance )
         elif event.key == pygame.K_o :
            # zoom out
            view.distance -= incr
            if debug : print( view.distance )
         elif event.key == pygame.K_z :
            # rotate theta radians around Z axis 
            if event.unicode == "Z" :
               # counterclockwise, from viewer's perspective
               fish.rotZ(-theta)
            else :            
               # clockwise, from viewer's perspective
               fish.rotZ(theta)
         elif event.key == pygame.K_y : 
            # rotate theta radians around Y axis
            if event.unicode == "Y" :
               # counterclockwise, viewed from above (+y)
               fish.rotY(-theta)
            else :            
               # clockwise, viewed from above (+y)
               fish.rotY(theta)
         elif event.key == pygame.K_x : 
            # rotate theta radians around X axis
            if event.unicode == "X" :
               # counterclockwise, viewed from +x perspective
               fish.rotX(-theta)
            else :            
               # clockwise, viewed from +x perspective
               fish.rotX(theta)
         elif event.key == pygame.K_UP :
            # move up
            fish.move((0.0, -incr, 0.0))
         elif event.key == pygame.K_DOWN :
            # move down
            fish.move((0.0, incr, 0.0))
         elif event.key == pygame.K_LEFT :
            # move left
            fish.move((-incr, 0.0, 0.0))
         elif event.key == pygame.K_RIGHT :
            # move right
            fish.move((incr, 0.0, 0.0))
         elif event.key == pygame.K_q : 
            # quit
            running = False
         
      if erase :
         screen.fill(bgcolor)

      if wireframe :
         for e in fish.edge :
            pygame.draw.aaline(screen, makeRGB(e[2], e[3], e[4]), view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])))
            if debug :
               print( fish.vertex[e[0]], fish.vertex[e[1]] )
               print( view.w2v(fish.vertex[e[0]]), view.w2v(fish.vertex[e[1]]) )
               print( view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])) )
               debug = False
      else :
         # z-sort faces
         fish.z_sort(sort_mode)
         for f in fish.face :
            # -1 in f[3] is a kludge to flag "backfaces"
            if (f[3] >= 0) :
                pygame.draw.polygon(screen, makeRGB(f[3], f[4], f[5]), [view.v2s(view.w2v(fish.vertex[f[0]])), view.v2s(view.w2v(fish.vertex[f[1]])), view.v2s(view.w2v(fish.vertex[f[2]]))])
   
      pygame.display.flip()
   
   # sleep   
   clock.tick(delay)

