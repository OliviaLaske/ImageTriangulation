# Imports
import math
import matplotlib
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np
from optparse import OptionParser
import os
from PIL import Image
import random
from scipy.spatial import Delaunay

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Command line options
parser = OptionParser()
parser.add_option('-d', '--d', dest='d',
                  action='store', type='int', default=60,
                  help='Density parameter')
parser.add_option('-f', '--file', dest='filepath', default=os.getcwd() + '/originalImages/waterLily.jpeg',
                  action='store', help='Image path for image to triangulate')
parser.add_option('-g', '--g', dest='finalname', default='triangulated.jpeg',
                  action='store', help='Final image name for saving')
parser.add_option('-s', '--s', dest='save',
                  action='store_true', help='Save final image')
parser.add_option('-t', '--t', dest='t',
                  action='store', type='int', default=50,
                  help='Threshold value')

(options, args) = parser.parse_args()

# Plot formatting
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
fontsize = 18
params = {
   'axes.labelsize': fontsize,
   'font.size': fontsize,
   'legend.fontsize': 12,
   'xtick.labelsize': fontsize,
   'ytick.labelsize': fontsize,
   'axes.titlesize': fontsize,
   'lines.linewidth': 1,  
   'xtick.direction': 'in',
   'ytick.direction': 'in',
   'font.family': 'Serif',
   'font.serif': 'Hoefler Text',
   'axes.grid': False,
   'figure.figsize': (6.75, 4),
   'figure.dpi': 250,
   'mathtext.fontset': 'cm'
}

for param in params.keys():
    matplotlib.rcParams[param] = params[param]

# Load image
threshold = options.t
densityReduction = options.d
image_orig = Image.open(options.filepath)
image = Image.open(options.filepath)
image_data = image.load()
image.show()

# Convert to greyscale
for i in range(image.width):
    for j in range(image.height):
        try:
            r, g, b, a = image.getpixel((i, j))
        except:
            r, g, b = image.getpixel((i, j))
        grey = 0.299*r + 0.587*g + 0.114*b
        image_data[i, j] = (int(grey), int(grey), int(grey))
image.show()

# Image Sharpening
# Define kernels
H = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]

# Initialize G and populate with 0s as placeholders
G = [[0]*image.height for i in range(image.width)]

maxG = 0
# Apply sharpening operator
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        x1 = H[0][0]*image.getpixel((i - 1, j - 1))[0]
        x2 = H[0][1]*image.getpixel((i, j - 1))[0]
        x3 = H[0][2]*image.getpixel((i + 1, j - 1))[0]
        x4 = H[1][0]*image.getpixel((i - 1, j))[0]
        x5 = H[1][1]*image.getpixel((i, j))[0]
        x6 = H[1][2]*image.getpixel((i + 1, j))[0]
        x7 = H[2][0]*image.getpixel((i - 1, j + 1))[0]
        x8 = H[2][1]*image.getpixel((i, j + 1))[0]
        x9 = H[2][2]*image.getpixel((i + 1, j + 1))[0]
        G_val = x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9
        G[i][j] = G_val
        
        if(G_val > maxG):
            maxG = G_val

# Replace pixel data
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        image_data[i, j] = (round(G[i][j]/maxG * 255), round(G[i][j]/maxG * 255), round(G[i][j]/maxG * 255))
image.show()

# Edge detection
# Define kernels
xKernel = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
yKernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

# Initialize Gx and Gy and populate with 0s as placeholders
Gx = [[0]*image.height for i in range(image.width)]
Gy = [[0]*image.height for i in range(image.width)]
G = [[0]*image.height for i in range(image.width)]
theta = [[0]*image.height for i in range(image.width)]

maxG = 0
# Apply Sobel operator
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        x1 = xKernel[0][0]*image.getpixel((i - 1, j - 1))[0]
        x2 = xKernel[0][1]*image.getpixel((i, j - 1))[0]
        x3 = xKernel[0][2]*image.getpixel((i + 1, j - 1))[0]
        x4 = xKernel[1][0]*image.getpixel((i - 1, j))[0]
        x5 = xKernel[1][1]*image.getpixel((i, j))[0]
        x6 = xKernel[1][2]*image.getpixel((i + 1, j))[0]
        x7 = xKernel[2][0]*image.getpixel((i - 1, j + 1))[0]
        x8 = xKernel[2][1]*image.getpixel((i, j + 1))[0]
        x9 = xKernel[2][2]*image.getpixel((i + 1, j + 1))[0]
        Gx_val = x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9
        Gx[i][j] = Gx_val
        
        y1 = yKernel[0][0]*image.getpixel((i - 1, j - 1))[0]
        y2 = yKernel[0][1]*image.getpixel((i, j - 1))[0]
        y3 = yKernel[0][2]*image.getpixel((i + 1, j - 1))[0]
        y4 = yKernel[1][0]*image.getpixel((i - 1, j))[0]
        y5 = yKernel[1][1]*image.getpixel((i, j))[0]
        y6 = yKernel[1][2]*image.getpixel((i + 1, j))[0]
        y7 = yKernel[2][0]*image.getpixel((i - 1, j + 1))[0]
        y8 = yKernel[2][1]*image.getpixel((i, j + 1))[0]
        y9 = yKernel[2][2]*image.getpixel((i + 1, j + 1))[0]
        Gy_val = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8 + y9
        Gy[i][j] = Gy_val
        
        G_val = math.sqrt(Gx_val**2 + Gy_val**2)
        G[i][j] = G_val
        
        try:
            theta[i][j] = math.atan(Gy_val/Gx_val)
        except:
            theta[i][j] = math.inf
        if(G_val > maxG):
            maxG = G_val

# Replace pixel data
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        image_data[i, j] = (round(G[i][j]/maxG * 255), round(G[i][j]/maxG * 255), round(G[i][j]/maxG * 255))
image.show()

# Determine vertices
S = []
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        if image_data[i, j][0] > threshold:
            S.append([i, j])
S = random.sample(S, round(len(S)/densityReduction)) # reduce density of point cloud
S.append([0, 0])
S.append([0, image.height - 1])
S.append([image.width - 1, 0])
S.append([image.width, image.height])
S = np.array(S)

# Randomly generate point cloud instead of using edge detection
# S = []
# numPoints = 1200
# xMin = 0
# xMax = image.width - 1
# yMin = 0
# yMax =  image.height - 1
# for i in range(numPoints):
#     x = random.randint(xMin, xMax)
#     y = random.randint(yMin, yMax)
#     if [x, y] in S:
#         x = random.randint(xMin, xMax)
#         y = random.randint(yMin, yMax)
#     S.append([x, y])
# S.append([xMin, yMin])
# S.append([xMin, yMax])
# S.append([xMax, yMin])
# S.append([xMax, yMax])
# S = np.array(S)

# Delaunay triangulation
# Currently uses scipy package
triangles = Delaunay(S)
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.invert_yaxis()
ax.triplot(S[:,0], S[:,1], triangles.simplices, color='black')
ax.set_axis_off()
plt.show()
# ax.plot(S[:,0], S[:,1], 'o', color='black') # plot vertices

# Color in image based on triangle centroids in original image overlay
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.invert_yaxis() # use image coordinates
for triangle in range(len(triangles.simplices)):
    vertices = S[triangles.simplices[triangle]]
    a = vertices[0]
    b = vertices[1]
    c = vertices[2]
    
    xs = vertices[:,0]
    ys = vertices[:,1]
    
    centroid = [(a[0] + b[0] + c[0])/3, (a[1] + b[1] + c[1])/3]
    color = image_orig.getpixel((centroid[0], centroid[1]))
    R = color[0]/255
    G = color[1]/255
    B = color[2]/255
    
    ax.fill(xs, ys, color=(R, G, B))
ax.set_axis_off()

if(options.save):
    print('here')
    image_name = options.finalname # replace with desired image name
    plt.savefig(os.getcwd() + '/triangulatedImages/' + image_name) # save image

plt.show()