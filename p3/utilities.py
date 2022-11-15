import numpy as np
from PIL import Image
import math

def draw_line(xs, ys, xe, ye, pixels, values):
    # make sure plot from left to right
    if xe < xs:
        xs, ys, xe, ye = xe, ye, xs, ys
    # whether from top to bottom or bottom to top
    yadd = 1
    if ye < ys:
        yadd = -1
    # if vertical
    if xs == xe:
        for y in range(ys, ye + 1):
            pixels[xs, y] = values
        return
    
    # calculate slope, using abs to avoid negative slope
    m = abs((ye - ys) / (xe - xs))
    # start to plot
    pixels[xs, ys] = values
    # plot along x axis
    if m < 1:
        dx = abs(xe - xs)
        dy = abs(ye - ys)
        dy2 = 2 * dy
        dyx = 2 * (dy - dx)
        
        tmpx = xs
        tmpy = ys
        pk = dy2 - dx
        while tmpx < xe:
            tmpx += 1
            if pk < 0:
                pk += dy2
            else:
                tmpy += yadd
                pk += dyx
            pixels[tmpx, tmpy] = values
    # plot along y axis
    else:
        dx = abs(xe - xs)
        dy = abs(ye - ys)
        dx2 = 2 * dx
        dxy = 2 * (dx - dy)
        
        tmpx = xs
        tmpy = ys
        pk = dx2 - dy
        while tmpx < xe:
            tmpy += yadd
            if pk < 0:
                pk += dx2
            else:
                tmpx += 1
                pk += dxy
            pixels[tmpx, tmpy] = values

def project_to_img(cur_df, img_size=1200, indices=None):
    img = Image.new('RGB', (img_size, img_size))
    pixels = img.load()
    curnp = cur_df.values
    if indices is None:
        for c1, c2 in curnp:
            pixels[c1, c2] = (255, 0, 0)
    else:
        for p1, p2, p3 in indices.values:
            draw_line(curnp[p1, 0], curnp[p1, 1], curnp[p2, 0], curnp[p2, 1], pixels, (255, 0, 0))
            draw_line(curnp[p1, 0], curnp[p1, 1], curnp[p3, 0], curnp[p3, 1], pixels, (255, 0, 0))
            draw_line(curnp[p3, 0], curnp[p3, 1], curnp[p2, 0], curnp[p2, 1], pixels, (255, 0, 0))
    return img
