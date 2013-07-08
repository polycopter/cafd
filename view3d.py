
# some readability consts for the View3d class:
# screen & viewport
left = 0
top = 1
right = 2
bottom = 3
# world
xmin = 0
xmax = 1
ymin = 2
ymax = 3
zmin = 4
zmax = 5
# eye
x = 0
y = 1
z = 2
      
class View3d :
   "methods related to projecting 3d objects onto a 2d screen"
   
   def __init__(self, screen, viewport, world, eye, distance) :
      # screen coords (left, top, right, bottom)
      self.screen = screen
      # "viewport" coords (l, t, r, b)
      self.viewport = viewport
      # world bounding box (xmin, xmax, ymin, ymax, zmin, zmax)
      self.world = world
      # world coordinates of the "viewer's eye" (x, y, z)
      self.eye = eye
      # z distance between the viewer's eye and the "viewport"
      self.distance = distance
      self.debug()
      
   def debug(self) :
      print( "screen:", self.screen )
      print( "viewport:", self.viewport )
      print( "world:", self.world )
      print( "eye:", self.eye )
      print( "distance:", self.distance )
      print( "w2v((1,1,1)):", self.w2v((1,1,1)) )
      print( "v2s((1,1)):", self.v2s((1,1)) )
      
   def w2v(self, point3) :
      "project a 3d point onto the 2d viewport"
      factor = (1.0 * self.distance)/(point3[z] - self.eye[z])
      vpX = point3[x] * factor
      vpY = point3[y] * factor
      return (vpX, vpY)
        
   def v2s(self, point2) :
      "convert from viewport coords to screen coords"
      relativeX = (point2[x] - self.viewport[left]) / (self.viewport[right] - self.viewport[left])
      screenX = self.screen[left] + relativeX * (self.screen[right] - self.screen[left])
      relativeY = (point2[y] - self.viewport[top]) / (self.viewport[bottom] - self.viewport[top])
      screenY = self.screen[top] + relativeY * (self.screen[bottom] - self.screen[top])      
      return (screenX, screenY)

# some methods related to 2d line intersections
      
def slope(p1, p2) :
   if ((p2[0] - p1[0])) == 0 :
      return 1000000000. # to do: NaN
   else :
      return (p2[1] - p1[1]) * 1. / (p2[0] - p1[0])
   
def y_intercept(slope, p1) :
   # to do: handle vertical lines
   return p1[1] - 1. * slope * p1[0]
   
def intersect(line1, line2) :
   # to do: handle parallel & vertical lines
   m1 = slope(line1[0], line1[1])
   print( 'm1: %d' % m1 )
   b1 = y_intercept(m1, line1[0])
   print( 'b1: %d' % b1 )
   m2 = slope(line2[0], line2[1])
   print( 'm2: %d' % m2 )
   b2 = y_intercept(m2, line2[0])
   print( 'b2: %d' % b2 )
   x = (b2 - b1) / (m1 - m2)
   y = m1 * x + b1
   y2 = m2 * x + b2
   print( '(x,y,y2) = %d,%d,%d' % (x, y, y2))
   return (int(x),int(y))
   
def segment_intersect(line1, line2) :
   intersection_pt = intersect(line1, line2)
   
   print( line1[0][0], line1[1][0], line2[0][0], line2[1][0], intersection_pt[0] )
   print( line1[0][1], line1[1][1], line2[0][1], line2[1][1], intersection_pt[1] )
   
   if (line1[0][0] < line1[1][0]) :
      if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0] :
         print( 'exit 1' )
         return None
   else :
      if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0] :
         print( 'exit 2' )
         return None
         
   if (line2[0][0] < line2[1][0]) :
      if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0] :
         print( 'exit 3' )
         return None
   else :
      if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0] :
         print( 'exit 4' )
         return None

   return intersection_pt
      
