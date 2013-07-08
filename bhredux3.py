#! /usr/bin/env python

import simple3d
import random
import sys
import math

def rotX(v, angle) :
    "rotate vertex v angle radians about the X axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newY = v[1]*c - v[2]*s
    newZ = v[1]*s + v[2]*c
    return [v[0], newY, newZ]

def rotY(v, angle) :
    "rotate vertex v angle radians about the Y axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newX = v[0]*c - v[2]*s
    newZ = v[0]*s + v[2]*c
    return [newX, v[1], newZ]
     
def rotZ(v, angle) :
    "rotate object angle radians about the Z axis"
    c = math.cos(angle)
    s = math.sin(angle)
    newX = v[0]*c - v[1]*s
    newY = v[0]*s + v[1]*c
    return [newX, newY, v[2]]
    
def getRandomColor() : 
    rgb = []
    rgb.append(random.random())
    rgb.append(random.random())
    rgb.append(random.random())
    return rgb

def getRandomDarkColor() : 
    rgb = []
    rgb.append(random.random()/2.)
    rgb.append(random.random()/2.)
    rgb.append(random.random()/2.)
    return rgb

def getRandomBlueColor() : 
    rgb = []
    rgb.append(random.random()/2.)
    rgb.append(random.random()/2.)
    rgb.append(random.random())
    return rgb

# radians for rotations
theta = math.radians(180/43)   # divide semicircle into 43 segments

# vertical displacement per cube
incr = 0.02
# cube size
edge_len = 0.3

fish = simple3d.Simple3d()
print('init...')

first_pt = [0.0, -1.0, 1.0]
fish.append_vertex(first_pt[0], first_pt[1], first_pt[2]) #0
alpha = 1
while alpha < (8*21) :
    new_pt = rotY(first_pt, alpha*theta)
    new_pt[1] += (alpha*incr)
    print('alpha, y, z = ', alpha, new_pt[1], new_pt[2])
    # vertices
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2]) #1
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1], new_pt[2]) #2
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1] + edge_len, new_pt[2]) #3
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1] + edge_len, new_pt[2] + edge_len) #4
    fish.append_vertex(new_pt[0], new_pt[1] + edge_len, new_pt[2] + edge_len) #5
    fish.append_vertex(new_pt[0], new_pt[1], new_pt[2] + edge_len) #6
    fish.append_vertex(new_pt[0] + edge_len, new_pt[1], new_pt[2] + edge_len) #7
    fish.append_vertex(new_pt[0], new_pt[1] + edge_len, new_pt[2]) #8
    # edges
    color = getRandomDarkColor()
    fish.append_edge(alpha, alpha + 1, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 1, alpha + 2, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 2, alpha + 3, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 3, alpha + 4, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 4, alpha + 5, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 5, alpha + 6, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha, alpha + 7, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha, alpha + 5, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 6, alpha + 1, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 6, alpha + 3, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 7, alpha + 4, color[0], color[1], color[2], 1.)
    fish.append_edge(alpha + 7, alpha + 2, color[0], color[1], color[2], 1.)
    # faces
    # front
    colorf = getRandomColor()
    fish.append_face(alpha, alpha + 2, alpha + 1, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha, alpha + 7, alpha + 2, colorf[0], colorf[1], colorf[2], 1.)
    # back
    colorf = getRandomColor()
    fish.append_face(alpha + 3, alpha + 4, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 3, alpha + 5, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
    # left
    colorf = getRandomColor()
    fish.append_face(alpha + 4, alpha + 7, alpha, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 4, alpha, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    # right
    colorf = getRandomColor()
    fish.append_face(alpha + 1, alpha + 3, alpha + 6, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 1, alpha + 2, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
    # top
    colorf = getRandomColor()
    fish.append_face(alpha + 2, alpha + 4, alpha + 3, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 2, alpha + 7, alpha + 4, colorf[0], colorf[1], colorf[2], 1.)
    # bottom
    colorf = getRandomColor()
    fish.append_face(alpha, alpha + 1, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    fish.append_face(alpha + 1, alpha + 6, alpha + 5, colorf[0], colorf[1], colorf[2], 1.)
    
    alpha += 8

# object gets named after the script that made it
fish.store_object("objects", sys.argv[0][0:-3])

print('done.')