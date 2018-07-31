'''
Created on Sep 1, 2010

@author: kkirsanov
'''
import pygame
import time
import math

def dst(x, y):
    if x >= y:
        return x - y
    else:
        return y - x
def dist1d(p1, p2):
    return math.sqrt((p1 - p2) ** 2)
def dist3d(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

pygame.init()
screen = pygame.display.set_mode((800, 600))

from optparse import OptionParser
parser = OptionParser()

parser.add_option("-f", default="6.jpg", dest="filename", help="image(/home/1.jpg)")
parser.add_option("-s", default="20", dest="sensivity", help="sensivity(1,2,...n)")
parser.add_option("-p", default="1", dest="count", help="pixels to overcrop(1,2,...n)")
parser.add_option("-d", default="25", dest="d", help="maximum distance between slices(1,2,...n)")
parser.add_option("-y", default="0", dest="symmetry", help="Symmetry (1,0)")
parser.add_option("-m", default="10", dest="m", help="maxcrop")

options, args = parser.parse_args()


image = pygame.image.load(options.filename).convert()
mindeviation = float(options.sensivity)
pixsize = int(options.count)
cd = int(options.d)
symmetry = int(options.symmetry)
maxcrop = int(options.m)

max = 640
x, y = map(float, image.get_size())

if x > y:
    k = float(x / 640)
else:
    k = float(y / 640)
image = pygame.transform.smoothscale(image, (x / k, y / k))
run = True

x1, y1, x2, y2 = [0] * 4
############################
#cropper
deviationsx = []
colorsx = []
deviationsy = []
colorsy = []


for x in range(0, image.get_width()):
    colors = []

    for y in range(0, image.get_height()):
        color = image.get_at((x, y))
        colors.append(sum(color[0:2]) / 3)
    median = sum(colors) / len(colors)
    deviation = math.sqrt(sum(map(lambda x:(median - x) ** 2, colors)) / len(colors))
    deviationsx.append (deviation)
    colorsx.append(median)

for y in range(0, image.get_height()):
    colors = []
    for x in range(0, image.get_width()):
        color = image.get_at((x, y))
        colors.append(sum(color[0:2]) / 3)
    median = sum(colors) / len(colors)
    deviation = math.sqrt(sum(map(lambda x:(median - x) ** 2, colors)) / len(colors))
    deviationsy.append (deviation)
    colorsy.append(median)

c = 0

for x in range(0, image.get_width() / 2):
    print deviationsx[x], mindeviation
    if x > 1:
        if dst(colorsx[x - 1], colorsx[x]) > cd:
            x1 = x
            break
             
    if deviationsx[x] > mindeviation:
        if c <= pixsize:
            x1 = x
            break
        c += 1
c = 0

for x in range(image.get_width() - 1, image.get_width() / 2, -1):
    if x < image.get_width() - 1:
        if dst(colorsx[x + 1], colorsx[x]) > cd:
            x2 = x
            break
    if deviationsx[x] > mindeviation:
        if c <= pixsize:
            x2 = x
            break
        c += 1


c = 0

for y in range(0, image.get_height() / 2):
    if y > 1:
        if dst(colorsy[y - 1], colorsy[y]) > cd:
            y1 = y
            break
    if deviationsy[y] > mindeviation:        
        if c <= pixsize:
            y1 = y
            break
        c += 1
        
c = 0
for y in range(image.get_height() - 1, image.get_height() / 2, -1):
    if y < image.get_height() - 1:
        if dst(colorsy[y + 1], colorsy[y]) > cd:
            y2 = y
            break
    if deviationsy[y] > mindeviation:
        if c <= pixsize:
            y2 = y
            break
        c += 1

print (x1, y1, x2, y2)

minx = min([image.get_width() - x2, x1])
miny = min([image.get_width() - y2, y1])


if symmetry:
    if x1 > minx:x1 = minx
    if image.get_width() - x2 > minx:x2 = image.get_width() - minx
    
    if y1 > miny:y1 = miny
    if image.get_height() - y2 > minx:y2 = image.get_height() - miny
while run:

    time.sleep(0.05)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.unicode == 'q':
                run = False
        
    screen.fill((10, 10, 10))
    screen.blit(image, (0, 0))
    pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2))
    pygame.draw.line(screen, (255, 0, 0), (x1, y2), (x2, y1))
    pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y1))
    pygame.draw.line(screen, (255, 0, 0), (x1, y2), (x2, y2))
    pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x1, y2))
    pygame.draw.line(screen, (255, 0, 0), (x2, y1), (x2, y2))
    
    pygame.display.flip()

pygame.quit()
