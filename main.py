#!/usr/bin/python
# -*- coding: utf-8 -*-
# для комментариев на русском
from meshOperations import *
import random as rand
import sys
# Генерация основной сетки, прямоугольника из прямоугольников, где
# a - ширина маленького прямоугольника
# b - высота маленького прямоугольника
# n - количество прямоугольников по x
# m - количество прямоугольников по y
#       0  -- n-1
#  0    --a--
#  |  |
#  |  b
# m-1 |
N = 0
M = 0

def initMainMesh(meshType, n, m, a, b, pn1 = -1, pn2 = -1, pn3 = -1, pn4 = -1):
    #print meshType, n, m, a, b, pn1, pn2, pn3, pn4
    global N
    global M
    N = n*a
    M = m*b
    for i in range(0,n):
        for j in range(0,m):
            if meshType == 1:
                # четыре вершины
                # конструктор точки принимает две координаты x и y, возвращает точку
                p1 = addPoint(i*a,   j*b)
                p2 = addPoint(i*a+a, j*b)
                p3 = addPoint(i*a+a, j*b+b)
                p4 = addPoint(i*a,   j*b+b)
                # пять линий
                # конструктор линии содержит два обязательных параметра
                # точки которые соединяет линия, возвращает линию
                if p1.y == 0:
                    l1 = addLine(p1, p2, False, pn1)
                else:
                    l1 = addLine(p1, p2)
                if p2.x == a*n:
                    l2 = addLine(p2, p3, False, pn2)
                else:
                    l2 = addLine(p2, p3)
                if p3.y == b*m:
                    l3 = addLine(p3, p4, False, pn3)
                else:
                    l3 = addLine(p3, p4)
                if p4.x == 0:
                    l4 = addLine(p4, p1, False, pn4)
                else:
                    l4 = addLine(p4, p1)

                # также содержит два необязательных параметра
                # "простота линии" - булевый параметр который просто добавляет линию
                # без учета пересечений и т.д., по умолчанию False
                # Четвертый параметр метка линии, physical line
                l5 = addLine(p2, p4)
                # два треугольника
                # конструктор поверхностей принимает список линий по очереди
                # порядок обхода значения не имеет
                s1 = addSurface([l1, l5, l4])
                # для добавления метки используется конструктор
                # принимающий поверхность и номер метки
                addSurfInPSurf(s1, 2)
                s2 = addSurface([l3, l5, l2])
                addSurfInPSurf(s2, 3)
            if meshType == 2:
                # четыре вершины
                # конструктор точки принимает две координаты x и y, возвращает точку
                p1 = addPoint(i*a,   j*b)
                p2 = addPoint(i*a+a, j*b)
                p3 = addPoint(i*a+a, j*b+b)
                p4 = addPoint(i*a,   j*b+b)
                # пять линий
                # конструктор линии содержит два обязательных параметра
                # точки которые соединяет линия, возвращает линию
                if p1.y == 0:
                    l1 = addLine(p1, p2, False, pn1)
                else:
                    l1 = addLine(p1, p2)
                if p2.x == a*n:
                    l2 = addLine(p2, p3, False, pn2)
                else:
                    l2 = addLine(p2, p3)
                if p3.y == b*m:
                    l3 = addLine(p3, p4, False, pn3)
                else:
                    l3 = addLine(p3, p4)
                if p4.x == 0:
                    l4 = addLine(p4, p1, False, pn4)
                else:
                    l4 = addLine(p4, p1)

                s1 = addSurface([l1, l2, l3, l4])
                # для добавления метки используется конструктор
                # принимающий поверхность и номер метки
                addSurfInPSurf(s1, 2)

def someLine(x1, y1, x2, y2, pn = -1):
    #print x1,y1,x2,y2
    p1 = addPoint(x1, y1)
    p2 = addPoint(x2, y2)
    addLine(p1, p2, False, pn, "Line", -1)

def process(line):
    a = []
    number = ''
    for s in line:
        if s in '1234567890.,-': # если символ - цифра, то собираем число
            if s == ",":
                number += "."
            else:
                number += s
        elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
            a.append(float(number))
            number = ''
    if number:  # если в конце строки есть число, выдаём его
        a.append(float(number))
    l = len(a)
    if line.find("#") > -1:
        return
    if line.find("mesh") > -1:
 #       print l
 #       if l == 5: initMainMesh(int(a[0]),int(a[1]),int(a[2]),a[3],a[4])
        if l == 9: initMainMesh(int(a[0]),int(a[1]),int(a[2]),a[3],a[4],int(a[5]),int(a[6]),int(a[7]),int(a[8]))
    if line.find("line") > -1:
        if l == 4: someLine(a[0],a[1],a[2],a[3])
        if l == 5: someLine(a[0],a[1],a[2],a[3],int(a[4]))
    if line.find("circle") > -1:
        p = addPoint(a[0],a[1])
        addCircle(p, a[2], a[3], a[4])
    if line.find("ellipse") > -1:
        p = addPoint(a[0],a[1])
        print a
        if l == 5: addEllipse(p, a[2], a[3], a[4])
        if l == 7: addEllipse(p, a[2], a[3], a[4], a[5], a[6])

setTime()
fileName = sys.argv[1]
inFile = open(fileName, "r")
while True:
  line = inFile.readline()
  if not line: break
  process(line)
inFile.close()
clearCircle()
clearMesh(N, M)
print getTime()
outMesh()

'''
# проверка пересечений линии и деления поверхности
initMainMesh(1, 1, 1, 1)
# функция для добавления линии по координатам
def someLine(x1, y1, x2, y2):
    print x1,y1,x2,y2
    p1 = addPoint(x1, y1)
    p2 = addPoint(x2, y2)
    addLine(p1, p2)

someLine(0.2, 0.1, 0.2, 0.9)
someLine(0.1, 0.4, 0.4, 0.7)
someLine(0.3, 0.5, 0.3, 0.9)
someLine(0.5, 0.7, 0.5, 0.9)
someLine(0.4, 0.8, 0.75, 0.8)
someLine(0.7, 0.75, 0.7, 0.95)
someLine(0.6, 0.9, 0.95, 0.9)
someLine(0.25, 0.85, 0.55, 0.85)
# проверка пересечений линии и деления поверхности
'''
'''
# проверка добавления эллипса
pt = addPoint(2, 1)
addEllipse(pt, 1.5, 1.0, 10)
def someLine(x1, y1, x2, y2):
    print x1,y1,x2,y2
    p1 = addPoint(x1, y1)
    p2 = addPoint(x2, y2)
    addLine(p1, p2)
someLine(0.0, 0.0, 1.0, 1.0)
'''
'''
# проверка пересечения эллипсов
pt1 = addPoint(0, 0)
addEllipse(pt1, 1.5, 1.0, 10)
pt2 = addPoint(2, 1)
addEllipse(pt2, 1.5, 1.0, 10)

'''
'''
# проверка пересечения эллипсов
pt1 = addPoint(0, 0)
addEllipse(pt1, 1.5, 1.0, 0)
pt2 = addPoint(2, 1)
addEllipse(pt2, 1.5, 1.1, 0)
'''
