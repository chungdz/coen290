from PIL import Image
import math
import collections
import pandas as pd
import numpy as np
from numpy.linalg import norm

# picture size factor
factor = 5
# define picture size
width=300 * factor
height=160 * factor
# define sphere radius
r1 = 50 * factor
r2 = 30 * factor
# define sphere surface color property
scolor1 = np.array([1, 1, 0])
scolor2 = np.array([0, 1, 1])
# define flour surface color property
fcolor = np.array([0.9, 0.9, 0.9])
# define ambient light
Iamb = np.array([50, 50, 50])
# define point light
IL = np.array([200, 200, 200])
# define sphere location
sloc1 = np.array([220 * factor, r1, 80 * factor])
sloc2 = np.array([120 * factor, r2, 80 * factor])
# define point light location
ploc = np.array([360 * factor, 200 * factor, 10 * factor])
# eye direction (from top to down)
V = np.array([0, 1, 0])

# accept iterable object representing RGB
# convert positive float value into integer in the range [0, 255]
def convert_to_color(nplist):
    newr = []
    for elem in nplist:
        newr.append(min(255, int(elem)))
    return tuple(newr)

# generate points for sphere
# sphere in 2D is just a circle, therefore generating points for a circle is enough
# the view is from top to down along y-axis, so the circle points are generated along x-axis and z-axis
# first generate edge points then use scan line to generate inside points (similar to assignment 1)
# for each generated point [x, z], the y coordinates can be calculated when the radius of the sphere is known
# there can be two y coordinates for each [x, z]
# since the view is from top to down, the points of half bottom is blocked by top bottom
# so I only pick up the larger y to form the final vector [x, y, z]
def generate_semisphere_3D(r, sloc):

    # generate circle edge along x-axis and z-axis
    # the y coordinates are unknown at this point, so by default they're all zeroes
    r2 = r ** 2
    d = 5/4 - r
    x = 0
    z = r
    points = [[x, 0, z], [z, 0, x]]

    # generate first quarter
    while x < z:
        if d < 0:
            d += 2 * x + 3
        elif d > 0:
            z -= 1
            d += 2 * x - 2 * z - 5

        x = x + 1
        points.append([x, 0, z])
        points.append([z, 0, x])

    points.append([int(r / math.sqrt(2)), 0, int(r / math.sqrt(2))])

    # check if all z have been generated
    spoints = set([x[2] for x in points])
    for z in range(0, r + 1):
        if z not in spoints:
            print(z)

    # generate rest quarters
    rest = []
    for xq, yq, zq in points:
        rest.append([xq, 0, -zq])
        rest.append([-xq, 0, zq])
        rest.append([-xq, 0, -zq])

    points += rest

    # generate points inside the edge
    # scan line
    zdict = collections.defaultdict(set)
    for x, y, z in points:
        zdict[z].add(x)
    # fill
    for cz, xset in zdict.items():
        xmin = min(xset)
        xmax = max(xset)
        for cx in range(xmin, xmax + 1):
            if cx in xset:
                continue
            points.append([cx, 0, cz])

    # generate y coordinate for all points
    for clist in points:
        y2 = r2 - clist[0] ** 2 - clist[2] ** 2
        if y2 > 0:
            clist[1] = int(math.sqrt(y2))
        else:
            clist[1] = 0

    # relocate based on sphere center location
    rpoints = np.array(points)
    rpoints += sloc
    
    return rpoints

# solve quadratic equation ax^2 + bx + c = 0
def solvingQuadratics(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        return []

    if abs(delta) < 1e-6:
        return [-b / (2 * a)]
    
    return [(-b + math.sqrt(delta)) / (2 * a), (-b - math.sqrt(delta)) / (2 * a)]

# check whether the line from point [x, y, z] to light source ploc is blocked by sphere
# sphere is defined by radius r and center location sloc
# https://math.stackexchange.com/questions/1939423/calculate-if-vector-intersects-sphere
def isBlocked(point, r, sloc):
    
    O = point
    E = ploc
    D = E - O
    Center = sloc

    a = sum(D * D)
    b = 2 * D[0] * (O[0] - Center[0]) + 2 * D[1] * (O[1] - Center[1]) + 2 * D[2] * (O[2] - Center[2])
    c = (O[0] - Center[0]) ** 2 + (O[1] - Center[1]) ** 2 + (O[2] - Center[2]) ** 2 - r ** 2

    for t in solvingQuadratics(a, b, c):
         if t >= 0 and t <= 1:
            return True
    
    return False

# calculate intensity for each pixel
# using the methods in class
# first check if the point is blocked
def cal_intensity(point, N, isFloor=False, isS2=False):
    
    # points of the floor may be blocked by two spheres
    if isFloor and (isBlocked(point, r1, sloc1) or isBlocked(point, r2, sloc2)):
        return Iamb
    # points of one sphere may be blocked by the other one
    if isS2 and isBlocked(point, r1, sloc1):
        return Iamb
    
    # same to the methods in the class
    L = ploc - point
    L = L / norm(L, ord=2)
    cos_theta = sum(L * N)
    
    if cos_theta <= 0:
        return Iamb
    
    Idiff = IL * cos_theta
    
    R = 2 * cos_theta * N - L
    R = R / norm(R, ord=2)
    cos_alpha = sum(R * V)
    if cos_alpha <= 0:
        return Iamb + Idiff
    
    Ispec = IL * cos_alpha ** 8
    return Iamb + Idiff + Ispec
