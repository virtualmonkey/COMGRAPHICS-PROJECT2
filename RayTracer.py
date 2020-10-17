from gl import Raytracer
from utils.gl_color import color
from utils.gl_math import V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random


brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 

boxMat = Material(texture = Texture('./materials/box.bmp'))
obsidianMat = Material(texture= Texture('./materials/obsidian.bmp'))
leavesMat = Material(texture= Texture('./materials/leaves.bmp'))
bigOakMat = Material(texture= Texture('./materials/log_big_oak.bmp'))
dirtMat = Material(texture= Texture('./materials/dirt.bmp'))
plankOakMat = Material(texture= Texture('./materials/planks_oak.bmp'))
purpleMat = Material(texture= Texture('./materials/purple.bmp'))
pumpkinMat = Material(texture= Texture('./materials/pumpkin_face_off.bmp'))



width = 720
height = 512
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('./materials/sunset.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
r.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.1)

# Objects
r.scene.append( AABB(V3(0, -1, -5), V3(10,0.5,10) , dirtMat))


r.scene.append( AABB(V3(-1, -0.5, -5), V3(0.5,0.5,0.5) , mirror))
r.scene.append( AABB(V3(-0.5, -0.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0, -0.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0.5, -0.5, -5), V3(0.5,0.5,0.5) , mirror))

r.scene.append( AABB(V3(-1, 0, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(-1, 0.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(-1, 1, -5), V3(0.5,0.5,0.5) , obsidianMat))

r.scene.append( AABB(V3(0.5, 0, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0.5, 0.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0.5, 1, -5), V3(0.5,0.5,0.5) , obsidianMat))

r.scene.append( AABB(V3(-1, 1.5, -5), V3(0.5,0.5,0.5) , mirror))
r.scene.append( AABB(V3(-0.5,  1.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0, 1.5, -5), V3(0.5,0.5,0.5) , obsidianMat))
r.scene.append( AABB(V3(0.5, 1.5, -5), V3(0.5,0.5,0.5) , mirror))

r.scene.append( AABB(V3(-0.25, 0.5, -5), V3(1,1.5,0.5) , purpleMat))
r.scene.append( AABB(V3(-0.17, 0.4, -3), V3(1,1,0.01) , glass))

r.scene.append( AABB(V3(0.75, -0.5, -4), V3(0.5,0.5,0.5) , pumpkinMat))


r.scene.append( AABB(V3(-1.5, -0.5, -3), V3(0.5,0.5,0.5) , bigOakMat ))
r.scene.append( AABB(V3(-1.5, 0, -3), V3(0.5,0.5,0.5) , bigOakMat ) )
r.scene.append( AABB(V3(-1.5, 0.5, -3), V3(0.5,0.5,0.5) , bigOakMat ))
r.scene.append( AABB(V3(-1.5, 1, -3), V3(0.5,0.5,0.5) , bigOakMat ))

r.scene.append( AABB(V3(-2, 1, -3), V3(0.5,0.5,0.5) , leavesMat ) )
r.scene.append( AABB(V3(-1.5, 1, -3.5), V3(0.5,0.5,0.5) , leavesMat ) )
r.scene.append( AABB(V3(-1, 1, -3), V3(0.5,0.5,0.5) , leavesMat ) )
r.scene.append( AABB(V3(-1.5, 1, -2.5), V3(0.5,0.5,0.5) , leavesMat ) )
r.scene.append( AABB(V3(-1.5, 1.5, -3), V3(0.5,0.5,0.5) , leavesMat ) )



r.rtRender()

r.glFinish('output.bmp')