from gl import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random



brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 

boxMat = Material(texture = Texture('box.bmp'))

earthMat = Material(texture = Texture('earthDay.bmp'))


width = 512
height = 512
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('envmap.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
r.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.1)

# Objects
#r.scene.append( Sphere(V3( 0, 0, -8), 2, brick) )
#r.scene.append( Sphere(V3( -0.5, 0.5, -5), 0.25, stone))
#r.scene.append( Sphere(V3( 0.25, 0.5, -5), 0.25, stone))


r.scene.append( AABB(V3(0, -3, -10), V3(5, 0.1, 5) , boxMat ) )
#r.scene.append( AABB(V3(1.5, 1.5, -5), V3(1, 1, 1) , boxMat ) )
#r.scene.append( AABB(V3(-1.5, 0, -5), V3(1, 1, 1) , boxMat ) )

r.scene.append( Sphere(V3( 0, 0, -8), 2, earthMat))



r.rtRender()

r.glFinish('output.bmp')





