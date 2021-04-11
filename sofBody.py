import numpy as np
import math as m

class point:
    def __init__(self):
        self.L = []
        self.L2 = []
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.m = 9
        
        self.dx = 0
        self.dy = 0
        self.dvx = 0
        self.dvy = 0
        
class Spring():
    def __init__(self):
        self.Ks = 9
        self.Kd = 5
        self.L0 = 40
        
def ForceRessort(i, j, spring):
    x1, y1, x2, y2 = P[i].x, P[i].y, P[j].x, P[j].y
    d = m.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    r = np.array([x2 - x1, y2 - y1])
    Fs = -spring.Ks * (d - spring.L0) * (r/d)
    return Fs

def SommeForce(j):
    F = [0, 0]
    for i in P[j].L:
        F += ForceRessort(i, j, springVoi)

    for i in P[j].L2:
        F += ForceRessort(i, j, springHor)
    
    F[1]+=P[j].m * 9.81
    return F

Points = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14]]
Points = [[1,2], [3, 4]]
P = {}
for i in Points:
    for x in i:
        P[x] = point()
        
springVoi = Spring()
springHor = Spring()
springHor.L0 = m.sqrt(2*(springVoi.L0**2))

collisionBox = 5
PositionDepart = 250
Espacement = 40
width = 500
height = 500

def Voisin(Point, index, indexLigne):
    for i in Points:
        for x in i:
            if x != Point:
                if abs(Points.index(i) - indexLigne) <= 1:
                    if abs(i.index(x) - index) <= 1:
                        if abs(i.index(x) - index) == 0:
                            P[Point].L.append(x)
                        
                        elif Points.index(i) == indexLigne:
                            P[Point].L.append(x)
                        else:
                            P[Point].L2.append(x)


def Init():
    countx = PositionDepart
    for i in Points:
        county = PositionDepart
        for x in i:
            P[x].x, P[x].y = countx, county
            county += Espacement
        countx += Espacement
            
    for i in Points:
        for x in i:
            Voisin(x, i.index(x), Points.index(i))

def CheckCollision(point):
    x = P[point].x
    y = P[point].y
    if x >= width or x+collisionBox >= width:
        P[point].x = width - collisionBox
        P[point].vx = (P[point].vx*-1) / 2
    if y+collisionBox >= height:
        P[point].y = height-collisionBox
        P[point].vy = (P[point].vy*-1) / 2
    if x <= 0:
        P[point].x = 0
        P[point].vx = (P[point].vx*-1) / 2
    if y <= 0:
        P[point].y = 0
        P[point].vy = (P[point].vy*-1) / 2
Init()
nbr = 0
def actu(nbr):
    nbr+=1
    can.delete('all')
    dt = 0.02
    for i in Points:
        for x in i:
            vx, vy = P[x].vx, P[x].vy
            m = P[x].m
            F = SommeForce(x)
            P[x].dx = vx * dt
            P[x].dy = vy * dt
            P[x].dvx = 1/m * F[0] * dt
            P[x].dvy = 1/m * F[1] * dt
            
            
    for i in Points:
        for x in i:
            CheckCollision(x)
            P[x].x += P[x].dx
            P[x].y += P[x].dy
            P[x].vx += P[x].dvx
            P[x].vy += P[x].dvy
            for z in P[x].L:
                can.create_line(P[x].x, P[x].y, P[z].x, P[z].y, fill = 'grey')
            for z in P[x].L2:
                can.create_line(P[x].x, P[x].y, P[z].x, P[z].y, fill = 'white')
            can.create_rectangle(P[x].x, P[x].y, P[x].x + collisionBox, P[x].y+collisionBox, fill = 'red', outline = 'red')
    window.after(10, actu, nbr)

import tkinter as tk

window = tk.Tk()

can = tk.Canvas(window, bg = '#192332', width = width, height = height)
can.grid()

window.after(2000, actu, nbr)

window.mainloop()