import math
import OzEngine as oz

bottom_right , bottom_left , top_right , top_left = 4, 1, 3, 2
left, right = 0, 1

def rotate_pixel(point:[int,int], center:[int,int], angle:float)->[int,int]:
  """
  point    is the point to rotate, in [x,y]
  center   is the point to rotate "point" around, in [x,y]
  angle    is the angle of the rotation
  """
  
  angle = math.radians(360-angle)

  px , py = point
  cx , cy = center
  
  x = px - cx
  y = py - cy
  
  new_x = x * math.cos(angle) - y * math.sin(angle)
  new_y = x * math.sin(angle) + y * math.cos(angle)
  
  new_x += center[0]
  new_y += center[1]
  
  return [round(new_x), round(new_y)]

def get_corner(shape:list, actual_corner:[int,int], actual_corner_type:int, new_corner_type:int) -> [int,int]:
  """
  shape                is the shape 
  actual_corner        is the corner of the shape, in [x,y]
  actual_corner_type   is the type of the corner
  new_corner_type      is the type of the new corner
  """
  cx, cy = actual_corner ; sx , sy = cx-round(len(shape[0])/2)+1 , cy+round(len(shape)/2)-1 ; rotate = 360-abs(int(actual_corner_type)-int(new_corner_type))*90
  nx , ny = rotate_pixel([cx,cy], [sx,sy], rotate)

  return [nx , ny]
  

def rotate_shape(shape:[[str,...],...], coor:[int,int], center:[int,int], angle:float) -> [[[str,...],...],[int,int]]:
  """
  shape    is the shape to rotate  HAVE TO BE A SQUARE !
  coor     is the bottom right corner of the shape, in [x,y]
  center   is the point to rotate the shape around, in [x,y]
  angle    is the angle of rotation
  """
  x , y = 0 , 0 ; cx , cy = (len(shape[0])-1)/2 , (len(shape)-1)/2 ; new = []; temp = []

  for todo in shape:
    for subtodo in todo:
      temp.append("")
    new.append(temp)
    temp = []
  
  for todo in shape:
    for subtodo in todo:
      nx , ny = rotate_pixel([x, y], [cx, cy], 360-angle)
      new[ny][nx] = subtodo
      
      x += 1
    x = 0
    y += 1

  return [new, coor]

def change_format(shape:[[str,...],...], coor:[int,int], coor_type:int) -> [[str,[int,int],...],...]:
  """
  shape   is the list of lists of strings
  coor    are the bottom right coordinates of the shape
  """
  new = ""; temp = []; idx = 0
  for todo in shape:
    for subtodo in todo:
      new += subtodo
    line_coor = [len(shape[idx])*coor_type+get_corner(shape, coor, bottom_right, coor_type+2)[0],idx+get_corner(shape, coor, bottom_right, coor_type+2)[1]-1]
    temp.append([new,line_coor])
    new = ""
    idx += 1

  return temp

class Format:
  __slots__ = "shape", "coor"
  def __init__(self, to_format):
    """
    init the format fuction
    """
    self.shape = to_format[0]
    self.coor = to_format[1]


  def oz_engine(x:object):
    """
    format your shape to be used with OZ Engine
    """
    next = change_format(x.shape, x.coor, bottom_left)

    return next

class OzEngine:
  def add_sprites(formated, canvas):
    sps = []
    for todo in formated:
      sps.append(oz.Sprite(canvas, todo[0], todo[1], str(todo)))