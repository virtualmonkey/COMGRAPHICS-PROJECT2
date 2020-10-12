import struct
import random
import numpy as np
from numpy import matrix, cos, sin, tan

from obj import Obj
from collections import namedtuple


OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z','w'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B.y - C.y)*(P.x - C.x) + (C.x - B.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        v = ( ((C.y - A.y)*(P.x - C.x) + (A.x - C.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def reflectVector(normal, dirVector):
    # R = 2 * (N dot L) * N - L
    reflect = 2 * np.dot(normal, dirVector)
    reflect = np.multiply(reflect, normal)
    reflect = np.subtract(reflect, dirVector)
    reflect = reflect / np.linalg.norm(reflect)
    return reflect

def refractVector(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    # Snell's Law
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        N = np.array(N) * -1

    eta = etai/etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0: # Total Internal Reflection
        return None
    
    R = eta * np.array(I) + (eta * cosi - k**0.5) * N
    return R / np.linalg.norm(R)

def fresnel(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1: # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2

BLACK = color(0,0,0)
WHITE = color(1,1,1)

class Raytracer(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

        self.camPosition = V3(0,0,0)
        self.fov = 60

        self.scene = []

        self.pointLight = None
        self.ambientLight = None

        self.envmap = None


    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def glClear(self):
        self.pixels = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]

        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glBackground(self, texture):

        self.pixels = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y, color = None):
        pixelX = ( x + 1) * (self.vpWidth  / 2 ) + self.vpX
        pixelY = ( y + 1) * (self.vpHeight / 2 ) + self.vpY

        if pixelX >= self.width or pixelX < 0 or pixelY >= self.height or pixelY < 0:
            return

        try:
            self.pixels[round(pixelY)][round(pixelX)] = color or self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.curr_color
        except:
            pass

    def glColor(self, r, g, b):

        self.curr_color = color(r,g,b)

    def glClearColor(self, r, g, b):

        self.clear_color = color(r,g,b)

    def glFinish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth,depth,depth))

        archivo.close()

    def rtRender(self):
        #pixel por pixel
        for y in range(self.height):
            for x in range(self.width):

                # pasar valor de pixel a coordenadas NDC (-1 a 1)
                Px = 2 * ( (x+0.5) / self.width) - 1
                Py = 2 * ( (y+0.5) / self.height) - 1

                #FOV(angulo de vision), asumiendo que el near plane esta a 1 unidad de la camara
                t = tan( (self.fov * np.pi / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                #Nuestra camara siempre esta viendo hacia -Z
                direction = V3(Px, Py, -1)
                direction = direction / np.linalg.norm(direction)

                self.glVertex_coord(x, y, self.castRay(self.camPosition, direction))


    def scene_intercept(self, orig, direction, origObj = None):
        tempZbuffer = float('inf')
        material = None
        intersect = None

        #Revisamos cada rayo contra cada objeto
        for obj in self.scene:
            if obj is not origObj:
                hit = obj.ray_intersect(orig, direction)
                if hit is not None:
                    if hit.distance < tempZbuffer:
                        tempZbuffer = hit.distance
                        material = obj.material
                        intersect = hit

        return material, intersect


    def castRay(self, orig, direction, origObj = None, recursion = 0):

        material, intersect = self.scene_intercept(orig, direction, origObj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.clear_color

        objectColor = np.array([material.diffuse[2] / 255,
                                material.diffuse[1] / 255,
                                material.diffuse[0] / 255])

        ambientColor = np.array([0,0,0])
        diffuseColor = np.array([0,0,0])
        specColor = np.array([0,0,0])

        reflectColor = np.array([0,0,0])
        refractColor = np.array([0,0,0])

        finalColor = np.array([0,0,0])

        shadow_intensity = 0

        # Direccion de vista
        view_dir = np.subtract(self.camPosition, intersect.point)
        view_dir = view_dir / np.linalg.norm(view_dir)

        if self.ambientLight:
            ambientColor = np.array([self.ambientLight.strength * self.ambientLight.color[2] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[1] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[0] / 255])

        if self.pointLight:
            # Sacamos la direccion de la luz para este punto
            light_dir = np.subtract(self.pointLight.position, intersect.point)
            light_dir = light_dir / np.linalg.norm(light_dir)

            # Calculamos el valor del diffuse color
            intensity = self.pointLight.intensity * max(0, np.dot(light_dir, intersect.normal))
            diffuseColor = np.array([intensity * self.pointLight.color[2] / 255,
                                     intensity * self.pointLight.color[1] / 255,
                                     intensity * self.pointLight.color[2] / 255])

            # Iluminacion especular
            reflect = reflectVector(intersect.normal, light_dir) # Reflejar el vector de luz

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** especularidad
            spec_intensity = self.pointLight.intensity * (max(0, np.dot(view_dir, reflect)) ** material.spec)
            specColor = np.array([spec_intensity * self.pointLight.color[2] / 255,
                                  spec_intensity * self.pointLight.color[1] / 255,
                                  spec_intensity * self.pointLight.color[0] / 255])


            shadMat, shadInter = self.scene_intercept(intersect.point,  light_dir, intersect.sceneObject)
            if shadInter is not None and shadInter.distance < np.linalg.norm(np.subtract(self.pointLight.position, intersect.point)):
                shadow_intensity = 1

        
        if material.matType == OPAQUE:
            # Formula de iluminacion, PHONG
            finalColor = (ambientColor + (1 - shadow_intensity) * (diffuseColor + specColor))
        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, np.array(direction) * -1)
            reflectColor = self.castRay(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = np.array([reflectColor[2] / 255,
                                     reflectColor[1] / 255,
                                     reflectColor[0] / 255])

            finalColor = reflectColor + (1 - shadow_intensity) * specColor

        elif material.matType == TRANSPARENT:

            outside = np.dot(direction, intersect.normal) < 0
            bias = 0.001 * intersect.normal
            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = reflectVector(intersect.normal, np.array(direction) * -1)
            reflectOrig = np.add(intersect.point, bias) if outside else np.subtract(intersect.point, bias)
            reflectColor = self.castRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = np.array([reflectColor[2] / 255,
                                     reflectColor[1] / 255,
                                     reflectColor[0] / 255])

            if kr < 1:
                refract = refractVector(intersect.normal, direction, material.ior)
                refractOrig = np.subtract(intersect.point, bias) if outside else np.add(intersect.point, bias)
                refractColor = self.castRay(refractOrig, refract, None, recursion + 1)
                refractColor = np.array([refractColor[2] / 255,
                                         refractColor[1] / 255,
                                         refractColor[0] / 255])


            finalColor = reflectColor * kr + refractColor * (1 - kr) + (1 - shadow_intensity) * specColor



        # Le aplicamos el color del objeto
        finalColor *= objectColor

        #Nos aseguramos que no suba el valor de color de 1
        r = min(1,finalColor[0])
        g = min(1,finalColor[1])
        b = min(1,finalColor[2])

        return color(r, g, b)


                











                











