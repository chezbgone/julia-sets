from PIL import Image, ImageDraw
import numpy as np
from scipy import interpolate
import time

t0 = time.time()

#size = (4500, 3000)
size = (9000, 6000)

eps = 0.000
(left, right, bot, top) = (-2, 1, -1, 1)
iterations = 256

img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

coordarr = np.fromfunction(lambda i, j: left + (right - left) * i/size[0] + bot * 1j + (top - bot)*1j * j/size[1], size)

def normsq(arr):
    return np.real(arr) ** 2 + np.imag(arr) ** 2

def compute(maxiter):
    plane = np.full(size, 0 + 0j)
    ptcolor = np.full(size, -1)
    # PRECOMPUTATION
    ptcolor[normsq(coordarr + 1) < 1/16] = maxiter
    ptcolor[normsq(coordarr + 1/4) < 1/4] = maxiter
    ####
    for i in range(maxiter):
        plane[ptcolor == -1] = np.square(plane[ptcolor == -1]) + coordarr[ptcolor == -1]
        ptcolor[np.logical_and(normsq(plane) > 4, ptcolor == -1)] = i
    ptcolor[ptcolor == -1] = maxiter
    return ptcolor

#P = iterate(iterations)
#draw.point(np.transpose(np.nonzero(np.abs(P) != np.inf)).flatten().tolist(), (255, 255, 255, 255))

P = compute(iterations)
print("computations done", time.time() - t0)

x = [100 * a for a in [0, 0.16, 0.42, 0.6425, 0.8575]]
r = [0, 32, 237, 255, 0]
g = [7, 107, 255, 170, 2]
b = [100, 203, 255, 0, 0]
rtck = interpolate.splrep(x, r)
gtck = interpolate.splrep(x, g)
btck = interpolate.splrep(x, b)
colors = [(interpolate.splev(i, rtck), interpolate.splev(i, gtck), interpolate.splev(i, btck), 255) for i in range(iterations)]

for color in range(iterations - 1):
    draw.point(np.transpose(np.nonzero(P == color)).flatten().tolist(), colors[color])
draw.point(np.transpose(np.nonzero(P == iterations)).flatten().tolist(), (0, 0, 0, 255))

img.save('mandelbrot_c.png')
print("wrote image", time.time() - t0)
