from PIL import Image, ImageDraw
import numpy as np
from scipy import interpolate
import time

t0 = time.time()

size = (4000, 4000)
(left, right, bot, top) = (-2, 2, -2, 2)
#(left, right, bot, top) = (-4, 4, -4, 4)
iterations = 256

img = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
imgname = 'julia_5.png'

inf = 100

def f(z):
    z[z == 1] = 100
    return z/(z - 1)
# julia_0: z ** 2 - 0.4 + 0.6j
# julia_1: z ** 2 - 0.7 - 0.45j
# julia_2: z ** 2 - 0.8j
# julia_3: z ** 2 + 0.286 + 0.01j
# julia_4: z ** 2 - 1

def normsq(arr):
    return np.real(arr) ** 2 + np.imag(arr) ** 2

def compute(maxiter):
    plane = np.fromfunction(lambda i, j: left + (right - left) * i/size[0] + bot * 1j + (top - bot)*1j * j/size[1], size)
    ptcolor = np.full(size, -1)
    ptcolor[normsq(plane) > inf] = 0
    for i in range(1, maxiter):
        plane[ptcolor == -1] = f(plane[ptcolor == -1])
        ptcolor[np.logical_and(normsq(plane) > inf, ptcolor == -1)] = i
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

img.save(imgname)
    print("wrote image", time.time() - t0)
