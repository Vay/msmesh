#!/usr/bin/python
# -*- coding: utf-8 -*-
# для комментариев на русском

from meshObjects import *

# adding point
# в метод добавления точки входит также проверка существования точки
# если точка в заданных координатах существует возвращается существующая точка
# также проверка на пересечение линии при добавлении новой точки
def addPoint(x, y):
    global pointsId
    global points
    global lines
    global surfaces
    point = Point()
    point.x = x
    point.y = y
    # check exist of point
    for pt in points:
        if pt.isEqual(point):
            return pt
    # if not exist, adds point
    point.id = pointsId
    pointsId = pointsId + 1
    points.append(point)
    # checks for crossing with lines
    for line in lines:
        if line.checkInLine(point):
            ptLines = getPLineWithLine(line)
            pLineNumber = -1
            if ptLines:
                pLineNumber = ptLines[0].id
            tl = addLine(point, line.end, True, pLineNumber, line.lineType, line.ellipseId)
            line.end = point
            for surf in surfaces:
                if line in surf.lines:
                    i = surf.lines.index(line)
                    if surf.lines[i-1].start == line.start or surf.lines[i-1].end == line.start:
                        i = i
                    else:
                        i = i - 1
                    surf.lines.insert(i + 1, tl)
                if line in surf.linesInSurface:
                    surf.linesInSurface.append(tl)
            break
    return point

def findLine(start, end, lines):
    tl = Line()
    f = False
    for line in lines:
        if line.start == start and line.end == end:
            tl = line
            f = True
        if line.start == end and line.end == start:
            tl = line
            f = True
    if f:
        return tl
    else:
        #print "can't find line"
        return False
# adding line
# также проверяется существование линии
# если simple == True, то идет добавление линии без поиска пересечений
# в случае пересечения с другими линиями функция рекурсивно вызывает себя
# если не находим пересечения то добавляем линию
# с учетом поверхностей
def addLine(start, end, simple = False, physicalNumber = -1, lineType = "Line", ellipseId = -1):
    global linesId
    global lines
    global surfaces
    global surfacesId
    global ellipses
    # check for exist the line
    for line in lines:
        if line.equal(start, end, lineType, ellipsesId):
            #if physicalNumber > 0:
                #addLineInPhysicalLine(line, physicalNumber)
            return line
    intersectSurf = False
    # check for intersection
    if not simple:
        tl = Line()
        tl.start = start
        tl.end = end
        tl.lineType = lineType
        tl.ellipseId = ellipseId
        for line in lines:
            pts = line.intersectionWithLine(tl)            
            if line.id == 12 and start.id+end.id==26 and np.abs(start.id-end.id)==4: print pts, "heeeeeeeeeey"
            if pts:
                point = pts[0]
                print point.out()
                if not line.consist(point):
                    newPoint = addPoint(point.x, point.y)
                    addLine(start, newPoint, False, physicalNumber, lineType, ellipseId)
                    addLine(newPoint, end, False, physicalNumber, lineType, ellipseId)
                    intersectSurf = True
                    break
                else:
                    if not tl.consist(point):
                        pt1 = line.end
                        if point.isEqual(line.start):
                            pt1 = line.start
                        addLine(start, pt1, False, physicalNumber, lineType, ellipseId)
                        addLine(pt1, end, False, physicalNumber, lineType, ellipseId)
                        intersectSurf = True
                        break
    # adding line
    if not intersectSurf:
        line = Line()
        line.lineType = lineType
        line.start = start
        line.end = end
        line.id = linesId
        linesId = linesId + 1
        line.ellipseId = ellipseId
        lines.append(line)
        if ellipseId > 0:
            for ell in ellipses:
                if ell.id == ellipseId:
                    ell.lines.append(line)
        # adding line in physical line
        if physicalNumber != -1:
            addLineInPhysicalLine(line, physicalNumber)
# разделение поверхности
        lineDivideSurface = False
        l = len(surfaces)
        for i in range(0, l):
            mmap = surfaces[i].getGraph()
            f1 = -1
            f2 = -1
            for key in mmap:
                if start in mmap[key]:
                    f1 = mmap[key].index(start)
                    key1 = key
                if end in mmap[key]:
                    f2 = mmap[key].index(end)
                    key2 = key
            if not (f1 == -1 or  f2 == -1):
                lineDivideSurface = True
                pts = surfaces[i].getPoints()
                newLineInSurf = surfaces[i].linesInSurface
                lineOfPaths = []
                startPoint = mmap[key1][f1]
                path1 = []
                while not startPoint in pts:
                    path1.append(startPoint)
                    for key in mmap:
                        if startPoint in mmap[key]:
                            tl = findLine(key, startPoint, newLineInSurf)
                            if tl:
                                lineOfPaths.append(tl)
                                newLineInSurf.remove(tl)
                            startPoint = key
                            break
                path1.append(startPoint)

                endPoint = mmap[key2][f2]
                path2 = []
                while not endPoint in pts:
                    path2.append(endPoint)
                    for key in mmap:
                        if endPoint in mmap[key]:
                            tl = findLine(key, endPoint, newLineInSurf)
                            if tl:
                                lineOfPaths.append(tl)
                                newLineInSurf.remove(tl)
                            endPoint = key
                            break
                path2.append(endPoint)

                spIndex = pts.index(startPoint)
                epIndex = pts.index(endPoint)
                directPath = []
                if len(path1) > 1:
                    for ii in range(len(path1)-1, 0, -1):
                        directPath.append(path1[ii-1])
                if len(path2) > 1:
                    for ii in range(0, len(path2)-1):
                        directPath.append(path2[ii])
                reversePath = []
                if len(path2) > 1:
                    for ii in range(len(path2)-1, 0, -1):
                        reversePath.append(path2[ii-1])
                if len(path1) > 1:
                    for ii in range(0, len(path1)-1):
                        reversePath.append(path1[ii])
                ii = min(spIndex, epIndex)
                jj = max(spIndex, epIndex) + 1
                newPts = pts[ii:jj]
                del pts[ii+1:jj-1]
                if spIndex < epIndex:
                    newPts = newPts + reversePath
                    pts = pts[0:ii+1] + directPath + pts[ii+1:len(pts)]
                else:
                    newPts = newPts + directPath
                    pts = pts[0:ii+1] + reversePath + pts[ii+1:len(pts)]
                surfaces[i].lines.append(line)
                newLines = surfaces[i].lines + lineOfPaths
                lineList1 = makeLinesFromPoints(pts, newLines)
                lineList2 = makeLinesFromPoints(newPts, newLines)
                surfaces[i].lines = makeLinesFromPoints(pts, newLines)
                newSurf = addSurface(lineList2)
                lineInSurf1 = []
                lineInSurf2 = []
                for tempLine in newLineInSurf:
                    if (inPolygonLines(tempLine.start, lineList1) and not tempLine.start in pts) \
                    or (inPolygonLines(tempLine.end, lineList1) and not tempLine.end in pts):
                        lineInSurf1.append(tempLine)
                    if (inPolygonLines(tempLine.start, lineList2) and not tempLine.start in newPts) \
                    or (inPolygonLines(tempLine.end, lineList2) and not tempLine.end in newPts):
                        lineInSurf2.append(tempLine)
                surfaces[i].linesInSurface = lineInSurf1
                newSurf.linesInSurface = lineInSurf2
                pSurfaces = checkSurfInPSurfs(surfaces[i])
                if pSurfaces:
                    for pSurface in pSurfaces:
                        addSurfInPSurf(newSurf, pSurface.id)
# пересечение поверхности
        # line in surface
        if not lineDivideSurface and not simple:
            for surf in surfaces:
                pts = surf.getPoints()
                if not (line in surf.lines):
                    if (inPolygonLines(line.start, surf.lines) and not line.start in pts) \
                    or (inPolygonLines(line.end, surf.lines) and not line.end in pts):
                        surf.linesInSurface.append(line)
        return line
# adding circle
def addCircle(center, radius, perforated = 0, pSurfaceId = -1):
    addEllipse(center, radius, radius, 0, perforated, pSurfaceId)    
def findLinesInPSurf(pLId):
    global pLines
    lines = []
    for pLine in pLines:
        if pLine.id == pLId:
            lines = pLine.lines[:]
    return lines

def makePointsFromLines(lines):
    pts = []
    pts.append(lines[0].start)
    lastI = 0
    while True:
        fPt = pts[len(pts)-1]
        for line in lines:
            if line.start == fPt:
                newPt = line.end
                lastI = lines.index(line)
                break
            if line.end == fPt and lines.index(line) <> lastI:
                newPt = line.start
                lastI = lines.index(line)
                break
        if newPt in pts: break
        pts.append(newPt)
    return pts

def findSurfsInEllipse(pts, lines):
    global surfaces
    surfs = []
    for surf in surfaces:
        flag = True
        ptsOfSurf = surf.getPoints()
        '''
        if surf.id == 4:
            print "ptsOfSurf"
            s = ''
            for element in ptsOfSurf:
                s = s + str(element.id) + ', '
            print s
            print "pts"
            s = ''
            for element in pts:
                s = s + str(element.id) + ', '
            print s
        '''
        for pt in ptsOfSurf:
            if not pt in pts:
                if not inPolygonLines(pt, lines):                    
                    flag = False
        if flag: surfs.append(surf)
    return surfs

def changePLines(ellLines, pSurfaceId):
    for line in ellLines:
        addLineInPhysicalLine(line, pSurfaceId)

# adding ellipse
def addEllipse(center, radiusA, radiusB, alpha = 0.0, perforated= 0, pSurfaceId = -1):
    global ellipses
    global ellipsesId
    global pLines
    if perforated:
        pLinesId = pSurfaceId
        pSurfaceId = -1
    else:
        pLinesId = -1
    print center, radiusA, radiusB, alpha, perforated, pSurfaceId
    deleted = not perforated
    talpha = np.deg2rad(alpha)
    sa = np.sin(talpha)
    ca = np.cos(talpha)
    ct = np.cos(0.0)
    st = np.sin(0.0)
    px = center.x + radiusA * ca * ct - radiusB * sa *st
    py = center.y + radiusA * sa * ct + radiusB * ca * st
    pointOnAxis = addPoint(px, py)
    ct = np.cos(np.pi/2.0)
    st = np.sin(np.pi/2.0)
    px = center.x + radiusA * ca * ct - radiusB * sa *st
    py = center.y + radiusA * sa * ct + radiusB * ca * st
    point1 = addPoint(px, py)
    ct = np.cos(np.pi)
    st = np.sin(np.pi)
    px = center.x + radiusA * ca * ct - radiusB * sa *st
    py = center.y + radiusA * sa * ct + radiusB * ca * st
    point2 = addPoint(px, py)
    ct = np.cos(np.pi * 3.0 / 2.0)
    st = np.sin(np.pi * 3.0 / 2.0)
    px = center.x + radiusA * ca * ct - radiusB * sa *st
    py = center.y + radiusA * sa * ct + radiusB * ca * st
    point3 = addPoint(px, py)
    ell = Ellipse()
    ell.center = center
    ell.a = radiusA
    ell.b = radiusB
    ell.alpha = alpha
    ell.pointOnAxis = pointOnAxis
    ell.id = ellipsesId
    ellipsesId = ellipsesId + 1
    ellipses.append(ell)
    ell.lines = []
    #print pointOnAxis.x, pointOnAxis.y
    #print point1.x, point1.y
    addLine(pointOnAxis, point1, False, 1000, 'Ellipse', ell.id)
    #print point1.x, point1.y
    #print point2.x, point2.y
    addLine(point1, point2, False, 1000, 'Ellipse', ell.id)
    #print point2.x, point2.y
    #print point3.x, point3.y
    addLine(point2, point3, False, 1000, 'Ellipse', ell.id)
    #print pointOnAxis.x, pointOnAxis.y
    #print point3.x, point3.y
    addLine(point3, pointOnAxis, False, 1000, 'Ellipse', ell.id)

    ellLines = findLinesInPSurf(1000)
    #print 1
    s = ''
    for element in ellLines:
        s = s + str(element.id) + ', '
    #print s
    pts = makePointsFromLines(ellLines)
    #print 2
    s = ''
    for element in pts:
        s = s + str(element.id) + ', '
    #print s
    ellSurfs = findSurfsInEllipse(pts, ellLines)
    #print 3
    s = ''
    for element in ellSurfs:
        s = s + str(element.id) + ', '
    #print s
    
    if pSurfaceId > 0:
        addSurfsInPSurf(ellSurfs, pSurfaceId)

    if pLinesId > 0:
        changePLines(ellLines, pLinesId)
    tLine = Surface()
    for pLine in pLines:
        if pLine.id == 1000:
            tLine = pLine
    pLines.remove(tLine)
    ell.deleted = deleted


# adding surface
def addSurface(lines):
    global surfaces
    global surfacesId
    surf = Surface()
    surf.lines = lines
    surf.linesInSurface = []
    surf.holes = []
    surf.id = surfacesId
    surfacesId = surfacesId + 1
    surfaces.append(surf)
    return surf
# добавление поверхности к физической поверхности
def  addSurfInPSurf(surf, id = -1):
    global pSurfs
    global pSurfsId
    if id < 0:
        id = pSurfsId + 100
        pSurfsId = pSurfsId + 1
    pSurf = PhysicalSurface()
    pSurf.surfaces = []
    for tpSurf in pSurfs:
        if tpSurf.id == id:
            pSurf = tpSurf
    pSurf.id = id
    pSurf.surfaces.append(surf)
    if not pSurf in pSurfs:
        pSurfs.append(pSurf)

def  addSurfsInPSurf(surfs, id = -1):
    for surf in surfs:
        addSurfInPSurf(surf, id)

def addLineInPhysicalLine(line, phId):
    global pLines
    tl = PhysicalLines()
    tl.lines = []
    isExist = False
    for pLine in pLines:
        if pLine.id == phId:
            tl = pLine
            isExist = True
    tl.id = phId
    if not line in tl.lines:
        tl.lines.append(line)
    if not isExist:
        pLines.append(tl)
# out in gmsh
def outMesh():
    global points
    global lines
    global surfaces
    global pSurfs
    global pLines
    global ellipses
    outFile = open("temp.geo", 'w')
    outFile.write("p1 = 0.1;\n")
    for point in points:
        if point.deleted == False: outFile.write(point.out())
    for line in lines:
        if line.deleted == False: outFile.write(line.out())
    for ell in ellipses:
        outFile.write(ell.out())
    for surf in surfaces:
        outFile.write(surf.out())
    for pSurf in pSurfs:
        outFile.write(pSurf.out())
    for pLine in pLines:
        outFile.write(pLine.out())
    outFile.close()

def clearMesh(n, m):
    global points
    global lines
    global surfaces
    global pSurfs
    global pLines
    global ellipses
    for point in points:
        if point.x > n or point.y > m:
            point.deleted = True
        if point.x < 0 or point.y < 0:
            point.deleted = True
    for line in lines:
        if line.start.deleted or line.end.deleted:
            line.deleted = True

def clearCircle():
    global points
    global lines
    global surfaces
    global pSurfs
    global pLines
    global ellipses
    pts = []
    print "clearCircle"
    for point in points:
        for ell in ellipses:
            if ell.deleted:
            #    if point.id == 9:
            #        s = ""
            #        for element in ell.lines:
            #            s = s + " " + str(element.id)
            #        print s
                lns = ell.getLines()
                #print inPolygonLines(point, lns),"inpolygoncheck"
                if inPolygonLines(point,  lns):
                    pts.append(point)
    #print pts
    for point in points:
        if not point in pts:
            #if point.id == 9:
            #    print "i am here"
            for line in lines:
                if line.consist(point):
                    for ell in ellipses:
                        if ell.deleted:
                            if line.ellipseId == ell.id:
                                pts.append(point)
    '''
    s = ""
    for pt in pts:
        s = s + " " + str(pt.id)
    print s
    '''
    #print pts
    for surf in surfaces:
        #print list(set(surf.getPoints()) - set(pts))
        #print surf.id
        if not list(set(surf.getPoints()) - set(pts)):
            surf.deleted = True
    k = 0
    for line in lines:        
        if line.deleted == False:
            f = True
            for surf in surfaces:
                if (line in surf.lines or line in surf.linesInSurface) and not surf.deleted:
                    f = False
                #if line in surf.linesInSurface:
                #    f = False
            if f: 
                line.deleted = True
                k = k + 1
    #print k
