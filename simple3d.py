import csv
import math
import random
import pygame
import view3d

def makeRGB(r,g,b) :
   return (math.floor(r*255),math.floor(g*255),math.floor(b*255))

class Simple3d :
   "3d object representation & manipulation"
   
   XCOORD = 0
   YCOORD = 1
   ZCOORD = 2
   # face color indices
   F_RED = 3
   F_GREEN = 4
   F_BLUE = 5
   F_ALPHA = 6
   # edge color indices
   E_RED = 2
   E_GREEN = 3
   E_BLUE = 4
   E_ALPHA = 5
   
   def __init__(self, path=None, name=None) :
      self.name = name
      self.path = path
      self.edge = []
      self.face = []
      self.vertex = []
      self.normal = []
      self.eye = (0.,0.,0.5) # default
   
   def debug(self) :
      "print the object data"
      print( "name:", self.name )
      print( "path:", self.path )
      print( "edge:" )
      for e in self.edge :
         print( e[0], e[1], e[2], e[3], e[4], e[5] )
      print( "face:" )
      for f in self.face :
         print( f[0], f[1], f[2], f[3], f[4], f[5], f[6] )
      print( "vertex:" )
      for v in self.vertex :
         print( v[0], v[1], v[2] )
      for n in self.normal :
         print( n[0], n[1], n[2] )
      
   def read_vertices(self, vfile) :
      "read the list of x,y,z values from objname.vertices"
      reader = csv.reader(open(vfile, 'r'), delimiter=',')
      for row in reader :
         self.append_vertex( float(row[0]), float(row[1]), float(row[2]) )
   
   def read_edges(self, efile) :
      "read the list of edges from objname.edges"
      reader = csv.reader(open(efile, 'r'), delimiter=',')
      for row in reader :
         self.append_edge( int(row[0]), int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]) )
   
   def read_faces(self, ffile) :
      "read the list of faces from objname.faces"
      reader = csv.reader(open(ffile, 'r'), delimiter=',')
      for row in reader :
         self.append_face( int(row[0]), int(row[1]), int(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]) )
   
   def compute_face_normals(self) :
      self.normal = []
      for f in self.face :
         # vector from 1st vertex in face to 2nd
         v1 = [self.vertex[f[0]][0] - self.vertex[f[1]][0], self.vertex[f[0]][1] - self.vertex[f[1]][1], self.vertex[f[0]][2] - self.vertex[f[1]][2]]
         # vector from 1st vertex in face to 3rd
         v2 = [self.vertex[f[0]][0] - self.vertex[f[2]][0], self.vertex[f[0]][1] - self.vertex[f[2]][1], self.vertex[f[0]][2] - self.vertex[f[2]][2]]
         # cross product (v1 X v2)
         self.append_normal(v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0])
   
   def load_object(self, path, name) :
      "read object data from 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open path/name.vertices
      self.read_vertices(fname + ".vertices")
      # open path/name.edges
      self.read_edges(fname + ".edges")
      # open path/name.faces
      self.read_faces(fname + ".faces")
      self.compute_face_normals()
      
   def store_object(self, path, name) :
      "write object data to 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open path/name.vertices
      self.write_vertices(fname + ".vertices")
      # open path/name.edges
      self.write_edges(fname + ".edges")
      # open path/name.faces
      self.write_faces(fname + ".faces")
      
   def write_vertices(self, vfile) :
      "write the list of x,y,z values to objname.vertices"
      writer = csv.writer(open(vfile, 'wb'), delimiter=',')
      for v in self.vertex :
         writer.writerow(v)
   
   def write_edges(self, efile) :
      "write the list of edges to objname.edges"
      writer = csv.writer(open(efile, 'wb'), delimiter=',')
      for e in self.edge :
         writer.writerow(e)
   
   def write_faces(self, ffile) :
      "write the list of faces to objname.faces"
      writer = csv.writer(open(ffile, 'wb'), delimiter=',')
      for f in self.face :
         writer.writerow(f)
   
   def append_vertex(self, x, y, z) :
      "add a 3D point to the object"
      self.vertex.append([x, y, z])

   def append_edge(self, v1, v2, r, g, b, a) :
      "add a pair of indices into the vertex list"
      self.edge.append([v1, v2, r, g, b, a])

   def append_face(self, v1, v2, v3, r, g, b, a) :
      "only triangles are currently supported"
      self.face.append([v1, v2, v3, r, g, b, a])
      
   def append_normal(self, x, y, z) :
      "add a normal to the list of face normals"
      self.normal.append([x, y, z])

   def connect_last(self, r, g, b, a) :
      "add an edge betwen the 2 most-recently added vertices"
      self.append_edge(len(self.vertex)-2, len(self.vertex)-1, r, g, b, a)
      
   def rotX(self, angle) :
      "rotate object angle radians about the X axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newY = v[1]*c - v[2]*s
         newZ = v[1]*s + v[2]*c
         newV.append([v[0], newY, newZ])
      self.vertex = newV
      self.compute_face_normals()
      # newN = []
      # for n in self.normal :
         # newY = n[1]*c - n[2]*s
         # newZ = n[1]*s + n[2]*c
         # newN.append([n[0], newY, newZ])
      # self.normal = newN
         
   def rotY(self, angle) :
      "rotate object angle radians about the Y axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[2]*s
         newZ = v[0]*s + v[2]*c
         newV.append([newX, v[1], newZ])
      self.vertex = newV
      self.compute_face_normals()
      # newN = []
      # for n in self.normal :
         # newX = n[0]*c - n[2]*s
         # newZ = n[0]*s + n[2]*c
         # newN.append([newX, n[1], newZ])
      # self.normal = newN
         
   def rotZ(self, angle) :
      "rotate object angle radians about the Z axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[1]*s
         newY = v[0]*s + v[1]*c
         newV.append([newX, newY, v[2]])
      self.vertex = newV
      self.compute_face_normals()
      # newN = []
      # for n in self.normal :
         # newX = n[0]*c - n[1]*s
         # newY = n[0]*s + n[1]*c
         # newN.append([newX, newY, n[2]])
      # self.normal = newN
         
   def move(self, vector) :
      "displace object by vector"
      newV = []
      for v in self.vertex :        
         newX = v[0] + vector[0]
         newY = v[1] + vector[1]
         newZ = v[2] + vector[2]
         newV.append([newX, newY, newZ])
      self.vertex = newV
      newN = []
      for n in self.normal :        
         newX = n[0] + vector[0]
         newY = n[1] + vector[1]
         newZ = n[2] + vector[2]
         newN.append([newX, newY, newZ])
      self.normal = newN
      
   def z_sort(self, sort_type) :
      newF = []
      faceZ = []
      index = 0
      # compute avg z value of @ face
      for f in self.face :
         if sort_type == "min" :
            zval = min(self.vertex[f[0]][2], self.vertex[f[1]][2])
            zval = min(zval, self.vertex[f[2]][2])
         elif sort_type == "max" :
            zval = max(self.vertex[f[0]][2], self.vertex[f[1]][2])
            zval = max(zval, self.vertex[f[2]][2])
         else :
            zval = (self.vertex[f[0]][2] + self.vertex[f[1]][2] + self.vertex[f[2]][2])/3.0
         faceZ.append([zval, index])
         index += 1
      # sort on zval
      faceZ.sort(key=lambda fz: fz[0], reverse=True)
      # normals must be sorted to match
      newN = []
      for f in faceZ :
         index = f[1]
         newF.append(self.face[index]) # [0], self.face[index][1], self.face[index][2], self.face[index][3], self.face[index][4], self.face[index][5], self.face[index][6]])
         newN.append(self.normal[index])
      self.face = newF
      self.normal = newN
   
   # added lines are opaque black by default
   def extrude_linear(self, p0, p1, num_new_pts, red = 0.0, green = 0.0, blue = 0.0, alpha = 1.0) :
      "add vertices to object by 'extruding' along a line"
      # to do: faces
      dx = float(p1[0] - p0[0])/num_new_pts
      dy = float(p1[1] - p0[1])/num_new_pts
      dz = float(p1[2] - p0[2])/num_new_pts
      for i in range(num_new_pts+1) :
         self.append_vertex( i*dx + p0[0], i*dy + p0[1], i*dz + p0[2] )
         if (i > 0) :            
            self.connect_last(red, green, blue, alpha)
			
   def copy_vertices(self, first, last, vector, scale) :
      "copy a set of vertices, displaced by a vector & scaled"
      for i in range(first,last+1) :
         newPt = self.vertex[i]
         newX = (newPt[0] + vector[0])*scale
         newY = (newPt[1] + vector[1])*scale
         newZ = (newPt[2] + vector[2])*scale
         self.append_vertex(newX, newY, newZ)
		
   def copy_edges(self, first, last, offset) :
      "replicate a set of edges, offsetting @ vertex index"
      for i in range(first,last+1) :
         e = self.edge[i]
         self.append_edge(e[0]+offset, e[1]+offset, e[2], e[3], e[4], e[5])

   def getRandomColor(self) : 
      rgb = []
      rgb.append(random.random())
      rgb.append(random.random())
      rgb.append(random.random())
      return rgb
         
   def getRandomDarkColor(self) : 
      rgb = []
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      return rgb

   def getRandomBlueColor(self) : 
      rgb = []
      rgb.append(random.random()/2.)
      rgb.append(random.random()/2.)
      rgb.append(random.random())
      return rgb

   def assign_random_colors(self) :
      "assign a random color to each edge & each face"
      for e in self.edge :
         color = self.getRandomColor()
         e[2] = color[0]
         e[3] = color[1]
         e[4] = color[2]
         # alpha         
      for f in self.face :
         color = self.getRandomColor()
         f[3] = color[0]
         f[4] = color[1]
         f[5] = color[2]
         # alpha         

   def assign_random_dark_colors(self) :
      "assign a random 'dark' color to each edge & each face"
      for e in self.edge :
         color = self.getRandomDarkColor()
         e[self.E_RED] = color[0]
         e[self.E_GREEN] = color[1]
         e[self.E_BLUE] = color[2]
         # alpha         
      for f in self.face :
         color = self.getRandomColor()
         f[self.F_RED] = color[0]
         f[self.F_GREEN] = color[1]
         f[self.F_BLUE] = color[2]
         # alpha         
         
   def assign_random_blue_colors(self) :
      "assign a random 'dark' color to each edge & each face"
      for e in self.edge :
         color = self.getRandomBlueColor()
         e[self.E_RED] = color[0]
         e[self.E_GREEN] = color[1]
         e[self.E_BLUE] = color[2]
         # alpha         
      for f in self.face :
         color = self.getRandomColor()
         f[self.F_RED] = color[0]
         f[self.F_GREEN] = color[1]
         f[self.F_BLUE] = color[2]
         # alpha         
   
   def set_eye(self, eye_coord) :
      self.eye = eye_coord
         
   def assign_grey_shade(self) :
      """ 
      assign a shade of grey to each face based on the angle
      between the face normal & vector from face to 'eye' coords 
      """
      index = 0
      for f in self.face :         
         f_center_x = (self.vertex[f[0]][0] + self.vertex[f[1]][0] + self.vertex[f[2]][0]) / 3.0
         f_center_y = (self.vertex[f[0]][1] + self.vertex[f[1]][1] + self.vertex[f[2]][1]) / 3.0
         f_center_z = (self.vertex[f[0]][2] + self.vertex[f[1]][2] + self.vertex[f[2]][2]) / 3.0
         eye_vector = (self.eye[0] - f_center_x, self.eye[1] - f_center_y, self.eye[2] - f_center_z)
         eye_vector_mag = math.sqrt(eye_vector[0]*eye_vector[0] + eye_vector[1]*eye_vector[1] + eye_vector[2]*eye_vector[2])
         normal_mag = math.sqrt(self.normal[index][0]*self.normal[index][0] + self.normal[index][1]*self.normal[index][1] + self.normal[index][2]*self.normal[index][2])
         # dot_product
         dot_product = eye_vector[0]*self.normal[index][0] + eye_vector[1]*self.normal[index][1] + eye_vector[2]*self.normal[index][2]
         # cos(theta) where theta is the angle between the face normal & vector from face to 'eye' coords
         dot_product /= (eye_vector_mag*normal_mag)
         print(dot_product)
         # to do: map better?
         # if dot_product < 0.0 : dot_product *= -1.0
         if dot_product > 1.0 : 
            shade = 1.0 
         else : 
            shade = dot_product
         self.face[index][self.F_RED] = shade
         self.face[index][self.F_GREEN] = shade
         self.face[index][self.F_BLUE] = shade
         index += 1
      print('------------')
      
   def draw(self, wireframe, screen, view, sort_mode) :
      if wireframe :
         for e in self.edge :
            pygame.draw.aaline(screen, makeRGB(e[2], e[3], e[4]), view.v2s(view.w2v(self.vertex[e[0]])), view.v2s(view.w2v(self.vertex[e[1]])))
      else :
         # z-sort faces
         self.z_sort(sort_mode)
         for f in self.face :
            # -1 in f[3] is a kludge to flag "backfaces"
            if (f[3] >= 0) :
                pygame.draw.polygon(screen, makeRGB(f[3], f[4], f[5]), [view.v2s(view.w2v(self.vertex[f[0]])), view.v2s(view.w2v(self.vertex[f[1]])), view.v2s(view.w2v(self.vertex[f[2]]))])
   	   
         
if __name__ == '__main__' :
   o = Simple3d()
   o.load_object('objects', 'test')
   o.debug()
   o.z_sort()
   o.debug()
   
   print( 'extrude 0,0,0 to 2,2,2 in 3' )
   o = Simple3d()
   o.extrude_linear( (0,0,0), (2.0,2.0,2.0), 3 )
   o.debug()
   
   print( 'extrude 0,0,0 to -2,-2,-2 in 3, red' )
   o.extrude_linear( (0,0,0), (-2.0,-2.0,-2.0), 3, 1.0, 0.0, 0.0, 1.0 )
   o.debug()
   
   # save number of vertices so far
   nv = len(o.vertex)
   print( 'copy vertices 0 through 3 displacing (2.0,0.0,0.0) scaling 1.2' )  
   o.copy_vertices(0,3,(2.0,0.0,0.0), 1.2)
   
   print( 'copy edges 0 through 2, offset by (#vertices)' )  
   o.copy_edges(0,2,nv)
   o.debug()
   o.store_object('objects', 'tst2')
