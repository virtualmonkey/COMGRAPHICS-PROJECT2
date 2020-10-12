from gl import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)

glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 


width = 256
height = 256
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('envmap.bmp')

r.pointLight = PointLight(position = V3(0,0,0), intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)

#r.scene.append( Sphere(V3( 1, 1, -10), 1.5, brick) )
#r.scene.append( Sphere(V3( 0, -1, -5),  1, glass) )
#r.scene.append( Sphere(V3(-3, 3, -10),  2, mirror) )

#r.scene.append( Plane( V3(-2,-3,0), V3(1,1,0), stone))

r.scene.append( AABB(V3(0, 1.5, -5), 1.5, stone ) )
r.scene.append( AABB(V3(1.5, -1.5, -5), 1.5, mirror ) )
r.scene.append( AABB(V3(-1.5, -1.5, -5), 1.5, glass ) )


r.rtRender()

r.glFinish('output.bmp')





