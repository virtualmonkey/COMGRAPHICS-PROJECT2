from gl import Raytracer
from utils.gl_color import color
from utils.gl_math import V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random


brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
grass = Material(diffuse = color(0.5, 1, 0), spec = 32)
glass = Material(diffuse = color(0.25, 1, 1), spec = 64)
coal = Material(diffuse = color(0.15,0.15,0.15), spec = 32)
eyes= Material(diffuse = color(0.90, 0.90, 0.90),spec = 64)

mirror = Material( spec = 64, matType = REFLECTIVE)



width = 512
height = 512

r = Raytracer(width,height)

r.glClearColor(0.2, 0.6, 0.8)

r.glClear()

r.envmap = Envmap('envmap.bmp')
r.pointLight = PointLight(position = (0,0,0), intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)



r.scene.append( Plane((0, -3.5, 0), (0,1,0), grass) )
r.scene.append( Plane((0, 3.5, 0), (0,1,0), stone) )
r.scene.append( Plane((0, 0, -10), (0,0,1), stone) )
r.scene.append( Plane(( -3.5,0, 0), (1,0,0), stone) )
r.scene.append( Plane(( 3.5, 0,0), (1,0,0), stone) )

r.scene.append( AABB((1.5, -1, -5), 1.5, stone ) )
r.scene.append( AABB((-1.5, 1, -5), 1.5, mirror ) )


r.rtRender()

r.glFinish('output.bmp')