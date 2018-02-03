#!/usr/bin/python
# -*- coding: utf-8 -*-
# для комментариев на русском
import math
import numpy as np
from matplotlib.pyplot import *
from shapely.geometry import LineString
from collections import defaultdict
import shapely.geometry.point as SPoint
import time

eps = 0.0001
points = []
pointsId = 1
lines = []
linesId = 1
ellipses = []
ellipsesId = 1
surfaces = []
surfacesId = 1
pSurfs = []
pSurfsId = 1
pLines = []

t = 0
def setTime():
    global t
    t = time.time()
def getTime():
    return time.time()-t
# ?????
# Base class
class Base:
    id = 0
    deleted = False

# Point class with id, x and y
class Point(Base):
    x = 0
    y = 0
    p = 0.5
# out in gmsh format
    def out(self):
        return "Point("+str(self.id)+")={"+str(self.x)+","+str(self.y)+",0, p1};\n"#str(self.p) +"};\n"
# compare with other point
    def isEqual(self, point):
        if (abs(point.x-self.x)+abs(point.y-self.y))<eps:
            return True
        return False
# distance to other point
    def distance(self, point):
        return math.sqrt((self.x-point.x)*(self.x-point.x)+(self.y-point.y)*(self.y-point.y))

    def getShapelyPoint(self):
        pt = SPoint.Point(self.x, self.y)
        return pt

def getAngle(x1,y1,x2,y2):
    a1, b1 = 1.0, 0.0
    a2, b2 = x2-x1, y2-y1
    if b2 == 0:
        if a2 > 0:
            return 0
        else:
            return 180
    la = np.sqrt(a1*a1+b1*b1)
    lb = np.sqrt(a2*a2+b2*b2)
    ab = a1 * a2 + b1 * b2
    cosa = ab/(la * lb)
    angleInRad = np.arccos(cosa)
    if b2 < 0:
        angleInRad = np.pi * 2 - angleInRad
    return np.rad2deg(angleInRad)

def ellipseArc(ellipse, alpha, beta, n = 1500):
    t = np.linspace(0, 3*np.pi, n, endpoint=True)
    st = np.sin(t)
    ct = np.cos(t)
    x  = []
    y  = []
    x0, y0, a, b, angle = ellipse
    sa = np.sin(angle)
    ca = np.cos(angle)
    p = np.empty((n, 2))
    p[:, 0] = x0 + a * ca * ct - b * sa * st
    p[:, 1] = y0 + a * sa * ct + b * ca * st
    i = 0
    if alpha > beta:
        beta = beta + 2 * np.pi
    if beta < angle:
        alpha = alpha + 2*np.pi
        beta = beta + 2*np.pi
    t = 0
    #print alpha, beta, 3*np.pi/n
    printtrue = False
    for pi in p:
        ang = np.deg2rad(getAngle(x0,y0,pi[0],pi[1]))
        if ang < t:
            ang = ang + 2*np.pi
        t = ang
        if ang >= alpha and ang <=beta:
            x.append(pi[0])
            y.append(pi[1])
            i = i + 1
    #print i
    result = np.empty((i, 2))
    result[:,0] = x
    result[:,1] = y
    return result

def intersectionLinePoint(line, point):
    lineS = LineString(line)
    pointS = point.getShapelyPoint()
    return lineS.distance(pointS)

def intersectionsLines(a, b):
    #plot(a[:,0], a[:,1])
    #plot(b[:,0], b[:,1])
    #show()
    ea = LineString(a)
    eb = LineString(b)
    mp = ea.intersection(eb)
    #print mp
    result = []
    if mp.geom_type == "MultiLineString":
        return False
    if mp.geom_type == "MultiPoint":
        for p in mp:
            result.append((p.x,p.y))
    #if type(mp) == list:
    #    x = [p.x for p in mp]
    #    y = [p.y for p in mp]
    if mp.geom_type == "Point":
        result.append((mp.x, mp.y))
    return result

# Line class with start and end point
class Line(Base):
    start = Point()
    end = Point()
    lineType = "Line"
    ellipseId = 0
    changed = False
    oldStart = Point()
    oldEnd = Point()
    ellipse = []
# out in gmsh format
    def out(self):
        if self.lineType == "Line":
            return "Line("+str(self.id)+")={"+str(self.start.id)+","+str(self.end.id)+"};\n"
        return ""
# check if point on the line ends
    def consist(self, point):
        if self.start.isEqual(point):
            return True
        if self.end.isEqual(point):
            return True
        return False
# check entrance point into the line
    def checkInLine(self, point):
        if self.lineType == "Line":
            if self.consist(point):
                return False
            a = point.distance(self.end)
            b = point.distance(self.start)
            c = self.start.distance(self.end)
            if abs(a + b - c)<eps:
                return True
            else:
                return False
        if self.lineType == "Ellipse":
            ellipse = self.getEllipse()
            result = intersectionLinePoint(ellipse, point)
            if result < eps:
                return True
            else:
                return False
        return False
# return line equation A*x + B*y + C = 0
    def getEquation(self):
        if self.lineType == "Line":
            A = self.start.y - self.end.y
            B = self.end.x - self.start.x
            C = self.start.x * self.end.y - self.end.x * self.start.y
            return A, B, -C
        else:
            return False

    def getLineString(self):
        line = LineString([(self.start.x, self.start.y),(self.end.x, self.end.y)])
        return line

    def getEllipsePoints(self):
        points = []
        tPoints = self.getEllipse()
        for point in tPoints:
            pt = Point()
            pt.x = point[0]
            pt.y = point[1]
            points.append(pt)
        return points

    def getEllipse(self):
        global ellipses
        if self.start.isEqual(self.oldStart) and self.end.isEqual(self.oldEnd):
            #print self.ellipse
            return self.ellipse
        ellipse = Ellipse()
        for ell in ellipses:
            if ell.id == self.ellipseId:
                ellipse = ell
        x0 = ellipse.center.x
        y0 = ellipse.center.y
        angle = np.deg2rad(ellipse.alpha)
        a = ellipse.a
        b = ellipse.b
        tempEllipse = (x0, y0, a, b, angle)
        startAngle = np.deg2rad(getAngle(x0, y0, self.start.x, self.start.y))
        endAngle = np.deg2rad(getAngle(x0, y0, self.end.x, self.end.y))
        c = ellipseArc(tempEllipse, startAngle, endAngle)
        self.ellipse = c
        self.oldStart = self.start
        self.oldEnd = self.end
        #print startAngle, endAngle, "Angle"
        #print self.start.x, self.start.y
        #print self.end.x, self.end.y
        #print c
        return c

# intersection between two line, return empty list if not find intersection
    def intersectionWithLine(self, line):
        boolForPrint = False
        if self.id == 12 and line.start.id+line.end.id==26 and np.abs(line.start.id-line.end.id)==4: 
            print "wtf???????????"
            print self.lineType
            print self.start.x, self.start.y
            print self.end.x, self.end.y
            print line.lineType
            print line.start.x, line.start.y
            print line.end.x, line.end.y
            boolForPrint = True
        isComplexObject = False   
        if self.lineType == "Line" and line.lineType == "Line":
            '''
            L1 = self.getEquation()
            L2 = line.getEquation()
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            l = []
            if boolForPrint 
            if D != 0:
                point = Point()
                point.x = Dx / D
                point.y = Dy / D
                if self.checkInLine(point) and line.checkInLine(point):
                    l.append(point)
            if self.id == 12 and line.start.id+line.end.id==26 and np.abs(line.start.id-line.end.id)==4: 

            return l
            '''
            obj1 = self.getLineString()
            obj2 = line.getLineString()
            isComplexObject = True
             
        if self.lineType == "Line" and line.lineType == "Ellipse":
            obj1 = self.getLineString()
            obj2 = line.getEllipse()
            isComplexObject = True
        if self.lineType == "Ellipse" and line.lineType == "Line":
            obj1 = self.getEllipse()
            obj2 = line.getLineString()
            isComplexObject = True
        if self.lineType == "Ellipse" and line.lineType == "Ellipse":
            obj1 = self.getEllipse()
            obj2 = line.getEllipse()
            isComplexObject = True
        if isComplexObject:
            someShapelyPoint = intersectionsLines(obj1, obj2)
            l = []
            if someShapelyPoint:
                if type(someShapelyPoint) == list:
                    for somePoint in someShapelyPoint:
                        point = Point()
                        point.x = somePoint[0]
                        point.y = somePoint[1]
                        if not self.consist(point):
                            l.append(point)
            return l
        else:
            print "something wrong"
    def equal(self, start, end, lineType, ellipsesId):
        if self.consist(start) and self.consist(end):
            if lineType == "Line" and self.lineType == "Line":
                return True
            if lineType == "Ellipse"  and self.lineType == "Ellipse"\
            and self.ellipseId == ellipsesId:
                return True
        return False

# Ellipse class not defined
class Ellipse(Base):
    center  = Point()
    a       = 0
    b       = 0
    alpha   = 0
    lines   = []
    pointOnAxis = Point()
    def out(self):
        #if self.deleted:
        #    return ""
        s = ""
        if self.center.deleted:
            s = s + self.center.out() + "\n"
        if self.pointOnAxis.deleted:
            s = s + self.pointOnAxis.out() + "\n"
        if self.a == self.b:
            for line in self.lines:
                if line.deleted == False:
                    s = s + "Circle(" + str(line.id) + ")={" + \
                    str(line.start.id) + "," + str(self.center.id) + "," + str(line.end.id) + "};\n"
        else:
            for line in self.lines:
                if line.deleted == False:
                    s = s + "Ellipsis(" + str(line.id) + ")={" + \
                    str(line.start.id) + "," + str(self.center.id) + "," +\
                    str(self.pointOnAxis.id) + ',' + str(line.end.id) + "};\n"
        return s
    def getLines(self):
        newLines = []
        newLines.append(self.lines[0])
        f = True
        while f:
            f = False
            for line in self.lines:
                if not line in newLines:
                    f = True
                    if newLines[len(newLines)-1].consist(line.start) or newLines[len(newLines)-1].consist(line.end):
                        newLines.append(line)
                        break
        return newLines

# Surface class contains a border line, line inside the surface
# and possibly the holes, but they are not defined
class Surface(Base):
    lines = []
    holes = []
    linesInSurface = []
# out in gmsh format
    def out(self):
        if self.deleted:
            return ""
        s = "Line Loop(" + str(self.id) + ")={"
        l = len(self.lines)
        # проход по линиям
        for i in range(0, l):
            j = i + 1
            if i == l - 1:
                j = 0
            # определение направления линии
            if self.lines[i].start == self.lines[j].start or self.lines[i].start == self.lines[j].end:
                s = s + "-"
            s = s + str(self.lines[i].id) + ", "
        s = s[:-2] + "};\n"
        s = s + "Plane Surface(" + str(self.id) + ") = {" + str(self.id) + "};\n"
        for line in self.linesInSurface:
            s = s + "Line{" + str(line.id) +"} In Surface{" + str(self.id) + "};\n"
        return s

# get in points format
    def getPoints(self):
        points = []
        # define the first point
        pt1 = self.lines[0].start
        pt2 = self.lines[0].end
        if self.lines[1].start == pt1 or self.lines[1].end == pt1:
            points.append(pt2)
            points.append(pt1)
        else:
            points.append(pt1)
            points.append(pt2)
        # end define first point
        for i in range(1, len(self.lines)-1):
            if self.lines[i].start == points[len(points)-1]:
                points.append(self.lines[i].end)
            else:
                points.append(self.lines[i].start)
        return points
# Этот метод возвращает поверхность как граф в виде мультимапа
# с учетом line in surfaces
# не реализован учет дыр внутри поверхности
# реализовать возникновение дыр при пересечении линий
    def getGraph(self):
        mmap = defaultdict(list)
        points = self.getPoints()
        for i in range(0,len(points)-1):
            mmap[points[i]].append(points[i+1])
        mmap[points[len(points)-1]].append(points[0])
        ptsInSurfaces = []
        for line in self.linesInSurface:
            if not line.start in ptsInSurfaces:
                ptsInSurfaces.append(line.start)
            if not line.end in ptsInSurfaces:
                ptsInSurfaces.append(line.end)
        mmap1 = mmap.copy()
        for key in mmap1:
            if key in ptsInSurfaces:
                queue = [key]
                #  проход в ширину если из точки идут линии внутрь поверхности
                for element in queue:
                    for line in self.linesInSurface:
                        if line.start.isEqual(element):
                            if not line.end in queue:
                                mmap[element].append(line.end)
                                queue.append(line.end)
                        if line.end.isEqual(element):
                            if not line.start in queue:
                                mmap[element].append(line.start)
                                queue.append(line.start)

        return mmap

# defined
class PhysicalLines(Base):
    lines = []
    def out(self):
        s = "Physical Line(" + str(self.id) + ") = {"
        for line in self.lines:
            if not line.deleted:
                s = s + str(line.id) + ', '
        s = s[:-2] + "};\n"
        return s

# defined
class PhysicalSurface(Base):
    surfaces = []
    def out(self):
        s = "Physical Surface(" + str(self.id) + ") = {"
        for surf in self.surfaces:
            if not surf.deleted:
                s = s + str(surf.id) + ', '
        s = s[:-2] + "};\n"
        if s == "Physical Surface(" + str(self.id) + ") =};\n":
            return ""
        return s
# https://ru.wikibooks.org/wiki/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2/%D0%97%D0%B0%D0%B4%D0%B0%D1%87%D0%B0_%D0%BE_%D0%BF%D1%80%D0%B8%D0%BD%D0%B0%D0%B4%D0%BB%D0%B5%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D0%B8_%D1%82%D0%BE%D1%87%D0%BA%D0%B8_%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE%D1%83%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA%D1%83
# для проверки находится ли точка внутри полигона используется алгоритм доступный выше по ссылке
# добавить проверку когда границой является дуга эллипса

def inPolygon(point, points):
    f = False
    l = len(points)
    for i in range(0, l):
        if (((points[i].y<=point.y and point.y<points[i-1].y) or \
        (points[i-1].y<=point.y and point.y<points[i].y)) and \
        (point.x > (points[i-1].x - points[i].x) * \
        (point.y - points[i].y) / (points[i-1].y - points[i].y) + points[i].x)):
            f = not f
    return f

def inPolygonLines(point, rlines):
    lines = rlines[:]
    points = []
    '''
    if point.id == 9:
        x = []
        y = []
        for line in lines:
            x.append(line.start.x)
            x.append(line.end.x)
            y.append(line.start.y)
            y.append(line.end.y)
        plot(x,y, "ro")
        show()
        '''
    # define the first point
    pts = []
    if lines[0].lineType == "Line":
        pts.append(lines[0].start)
        pts.append(lines[0].end)
        #print "L"
    if lines[0].lineType == "Ellipse":
        lns = lines[0].getEllipsePoints()
        pts.append(lines[0].start)
        pts = pts + lns
        pts.append(lines[0].end)
        #print pts, lns

    points = pts
    if lines[1].start == pts[0] or lines[1].end == pts[0]:
        points.reverse()

    lines.append(lines[0])
    # end define first point
    for i in range(1, len(lines)-1):
        if lines[i].start == points[len(points)-1]:
            if lines[i].lineType == "Line":
                points.append(lines[i].end)
            if lines[i].lineType == "Ellipse":
                lns = lines[i].getEllipsePoints()
                points = points + lns
                points.append(lines[i].end)
        else:
            if lines[i].lineType == "Line":
                points.append(lines[i].start)
            if lines[i].lineType == "Ellipse":
                lns = lines[i].getEllipsePoints()
                lns.reverse()
                points = points + lns
                points.append(lines[i].start)
    '''
    if point.id == 9:
        x = []
        y = []
        for pt in points:
            x.append(pt.x)
            y.append(pt.y)
        plot(point.x, point.y, "ro")
        plot(x,y)
        print point.x, point.y, "9"
        show()
    '''

    f = inPolygon(point, points)
    return f

# remakes surface from points
def makeLinesFromPoints(pts, lines):
    newLines = []
    l = len(pts)
    for i in range(0, l):
        j = i + 1
        if j == l:
            j = 0
        tl = Line()
        f = False
        for line in lines:
            if line.start == pts[i] and line.end == pts[j]:
                tl = line
                f = True
            if line.start == pts[j] and line.end == pts[i]:
                tl = line
                f = True
        if f:
            newLines.append(tl)
    return newLines
# метод возвращает список физических поверхностей
# в которые входит заданная поверхность
def checkSurfInPSurfs(surf):
    global pSurfs
    surfs = []
    for pSurf in pSurfs:
        if surf in pSurf.surfaces:
            surfs.append(pSurf)
    return surfs
# метод возвращает список физических линий
# в которые входит заданная линия
def getPLineWithLine(line):
    global pLines
    lines = []
    for pLine in pLines:
        if line in pLine.lines:
            lines.append(pLine)
    return lines
