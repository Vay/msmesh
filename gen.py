import random
import sys
import importlib
import numpy as np
mesh = {}
lines = []
circles = []
ellipses = []
maxSizeX = 0
minSizeX = 0
maxSizeY = 0
minSizeY = 0
if len(sys.argv) > 1:
    inFileName = sys.argv[1]
else:
    inFileName = "in"
if len(sys.argv) > 2:
    outFileName = sys.argv[2]
else:
    outFileName = "output.txt"
outFile = open(outFileName, 'w')

def check(map, key):
    try:
        return map[key]
    except KeyError:
        print key+" not found"
        return False

def getValues():
    global mesh
    global lines
    global circles
    global ellipses 
    if check(data, "seed"):
        random.seed(data["seed"])
    if check(data, "mesh"):
        mesh = data["mesh"]
    if check(data, "lines"):
        lines = data["lines"]
    if check(data, "circles"):
        circles = data["circles"]
    if check(data, "ellipses"):
        ellipses = data["ellipses"]

def printMesh(mesh):    
    global maxSizeX
    global maxSizeY
    s = "mesh "    
    if check(mesh, "type"): 
        s = s + str(mesh["type"]) + " "
    else:
        s = s + "1 "        
    if check(mesh, "n"):
        s = s + str(mesh["n"]) + " "
        maxSizeX = mesh["n"]
    else:
        s = s + "1 "
        maxSizeX = 1
    if check(mesh, "m"):
        s = s + str(mesh["m"]) + " "
        maxSizeY = mesh["m"]
    else:
        s = s + "1 "
        maxSizeY = 1
    if check(mesh, "width"):
        s = s + str(mesh["width"]) + " "
        maxSizeX = maxSizeX * mesh["width"]
    else:
        s = s + "1 "
        maxSizeX = maxSizeX * 1
    if check(mesh, "height"):
        s = s + str(mesh["height"]) + " "
        maxSizeX = maxSizeX * mesh["height"]
    else:
        s = s + "1 "
        maxSizeY = maxSizeY * 1
    if check(mesh, "bottomPhysical"):
        s = s + str(mesh["bottomPhysical"]) + " "
    else:
        s = s + "1 "
    if check(mesh, "rightPhysical"):
        s = s + str(mesh["rightPhysical"]) + " "
    else:
        s = s + "1 "
    if check(mesh, "topPhysical"):
        s = s + str(mesh["topPhysical"]) + " "
    else:
        s = s + "1 "
    if check(mesh, "leftPhysical"):
        s = s + str(mesh["leftPhysical"]) + " "
    else:
        s = s + "1 "    
    s = s + "\n"
    outFile.write(s)

def printLine(element):    
    count = 1
    if check(element, "count"):
        count = element["count"]    
    s = ""
    min = 0
    max = np.square(maxSizeX - minSizeX) + \
        np.square(maxSizeY - minSizeY)
    max = np.sqrt(max)    
    if check(element, "size"):
        min = element["size"]["min"]        
        max = element["size"]["max"]
    min = np.square(min)
    max = np.square(max)
    minsx = minSizeX
    maxsx = maxSizeX
    minsy = minSizeY
    maxsy = maxSizeY
    if check(element, "area"):
        minsx = element["area"]["minx"]
        minsx = element["area"]["maxx"]
        minsx = element["area"]["miny"]
        minsx = element["area"]["maxy"]
    ph = -1
    if check(element, "physical"):
        ph = element["physical"]
    for i in range(count):        
        while True:
            x1 = random.random() * (maxsx - minsx) + minsx
            x2 = random.random() * (maxsx - minsx) + minsx
            y1 = random.random() * (maxsy - minsy) + minsy
            y2 = random.random() * (maxsy - minsy) + minsy
            a = x1 - x2
            b = y1 - y2
            d = a * a + b * b 
            if d > min and  d < max:
                s = s + "line " + str(x1) + " " \
                + str(y1) + " " + str(x2) + " " + str(y2) + " "
                break
        if ph > 0:
            s = s + str(ph) + " "
        s = s + "\n"
    outFile.write(s)

def printCircle(element):        
    count = 1
    if check(element, "count"):
        count = element["count"]    
    s = ""
    min = 0
    max = np.square(maxSizeX - minSizeX) + \
        np.square(maxSizeY - minSizeY)
    max = np.sqrt(max) / 2
    if check(element, "size"):
        min = element["size"]["min"]        
        max = element["size"]["max"]    
    minsx = minSizeX
    maxsx = maxSizeX
    minsy = minSizeY
    maxsy = maxSizeY
    if check(element, "area"):
        minsx = element["area"]["minx"]
        maxsx = element["area"]["maxx"]
        minsy = element["area"]["miny"]
        maxsy = element["area"]["maxy"]
    ph = -1
    if check(element, "physical"):
        ph = element["physical"]
    perforated = False
    if check(element,"perforated"):
        perforated = element["perforated"]
    for i in range(count):                
        x1 = random.random() * (maxsx - minsx) + minsx
        y1 = random.random() * (maxsy - minsy) + minsy
        r = random.random() * (max - min) + min            
        s = s + "circle " + str(x1) + " " \
        + str(y1) + " " + str(r) + " "
        if perforated:
            s = s + "0 "
        else:
            s = s + "1 "
        if ph > 0:
            s = s + str(ph) + " "        
        s = s + "\n"
    outFile.write(s)

def printEllipse(element):    
    count = 1
    if check(element, "count"):
        count = element["count"]    
    s = ""
    minA = 0
    maxA = np.square(maxSizeX - minSizeX) + \
        np.square(maxSizeY - minSizeY)
    maxA = np.sqrt(maxA) / 2    
    if check(element, "sizeA"):
        minA = element["sizeA"]["min"]        
        maxA = element["sizeA"]["max"]
    minB = 0
    maxB = np.square(maxSizeX - minSizeX) + \
        np.square(maxSizeY - minSizeY)
    maxB = np.sqrt(maxB) / 2    
    if check(element, "sizeB"):
        minB = element["sizeB"]["min"]        
        maxB = element["sizeB"]["max"]    
    minsx = minSizeX
    maxsx = maxSizeX
    minsy = minSizeY
    maxsy = maxSizeY
    if check(element, "area"):
        minsx = element["area"]["minx"]
        maxsx = element["area"]["maxx"]
        minsy = element["area"]["miny"]
        maxsy = element["area"]["maxy"]
    minAngle = 0
    maxAngle = 0
    if check(element, "angle"):
        minAngle = element["angle"]["min"]        
        maxAngle = element["angle"]["max"]    
    ph = -1
    if check(element, "physical"):
        ph = element["physical"]
    perforated = False
    if check(element,"perforated"):
        perforated = element["perforated"]
    for i in range(count):                
        x1 = random.random() * (maxsx - minsx) + minsx
        y1 = random.random() * (maxsy - minsy) + minsy
        ra = random.random() * (maxA - minA) + minA            
        rb = random.random() * (maxB - minB) + minB     
        print rb       
        angle = random.random() * (maxAngle - minAngle) + minAngle
        s = s + "ellipse " + str(x1) + " " \
        + str(y1) + " " + str(ra) + " " + str(rb) + " " + str(angle) + " "        
        if perforated:
            s = s + "0 "
        else:
            s = s + "1 "
        if ph > 0:
            s = s + str(ph) + " "
        s = s + "\n"
    outFile.write(s)

lib = importlib.import_module(inFileName) 
data = lib.dictionary
getValues()
printMesh(mesh)
for line in lines:
    printLine(line)
for circle in circles:
    printCircle(circle)
for ellipse in ellipses:
    printEllipse(ellipse)
