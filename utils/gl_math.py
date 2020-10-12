from collections import namedtuple
import math


V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z','w'])
PI = 3.141592653589793

def deg2rad(degrees):
	radians = degrees * (PI/180)
	return radians

def substract(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def sum(v0, v1):
    return V3(v0.x+v1.x, v0.y+v1.y, v0.z+v1.z)

def sumNPArray(v0, v1):
    return [v0[0]+v1[0], v0[1]+v1[1], v0[2]+v1[2]]

def substractNPArray(v0, v1):
    return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]

def normNPArray (v0):
    vLength = lengthNPArray(v0)
    if not vLength:
        return [0, 0, 0]

    return [v0[0]/vLength, v0[1]/vLength, v0[2]/vLength]

def magnitudeNpArray(x): 
    return math.sqrt(dotNPArray(x,x))
    
def dotNPArray(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def lengthNPArray(v0):
    return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5

def multiplyConstant(c, v0):
    return [v0[0]*c,v0[1]*c,v0[2]*c]

def multiplyColor(v1,v2):
    return [v1[0]*v2[0], v1[1]*v2[1], v1[2]*v2[2]]

def norm(v0):
    vLength = length(v0)
    if not vLength:
        return V3(0, 0, 0)

    return V3(v0.x/vLength, v0.y/vLength, v0.z/vLength)
    
def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def cross(v0, v1):
    return V3(
        v0.y * v1.z - v0.z * v1.y,
        v0.z * v1.x - v0.x * v1.z,
        v0.x * v1.y - v0.y * v1.x,
    )
# La lógica par sacar la matriz inversa fue extraída de 
# https://stackoverflow.com/a/39881366/11168233
def eliminate(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]

def gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                print("It's not invertible :C")
                return -1
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a

def inverse(a):
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret

# La lógica para operar matrices fue extraída de
# https://www.programiz.com/python-programming/examples/multiply-matrix

def multiplyMatrices(matrix0, matrix1):
	matrix = [[0 for x in range(len(matrix0))] for y in range(len(matrix1[0]))]
	for i in range(len(matrix0)):
		for j in range(len(matrix1[0])):
			for k in range(len(matrix1)):
				matrix[i][j] += matrix0[i][k] * matrix1[k][j]
	return matrix

def matrixDotVector(matrix0, v0):
	matrix = [[0 for x in range(len(matrix0))] for y in range(1)]
	for i in range(len(matrix0)):
		for j in range(1):
			for k in range(len(v0)):
				matrix[0][i] += matrix0[i][k] * v0[k]
	return matrix
