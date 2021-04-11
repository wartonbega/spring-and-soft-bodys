import math
import numpy as np

class point:
    def __init__(self):
        self.L = []
        self.L2 = []
        self.Mouse = []
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.m = 5
        
        self.dx = 0
        self.dy = 0
        self.dvx = 0
        self.dvy = 0
        
class Spring():
    def __init__(self):
        self.Ks = 30
        self.Kd = 10
        self.L0 = 30

def phi(d, L0):
    if d > L0/2:
        return 0
    else:
        return math.exp((-1/(d-L0/2)**2 + 1/d**2)*alpha)
    
def ForceRessort(i, j, spring):
    x1, y1, x2, y2 = P[i].x, P[i].y, P[j].x, P[j].y
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    r = np.array([x2 - x1, y2 - y1])
    VV  = np.array([P[j].vx - P[i].vx, P[j].vy - P[i].vy ])
    #V = m.sqrt((P[i].vx - P[j].vx)**2 + (P[i].vy - P[j].vy)**2)
    VD = (VV[0] * r[0] + VV[1] * r[1]) / d # Projection de V
    Ks = spring.Ks
    Kd = spring.Kd
    L0 = spring.L0
    
    Fs = -Ks * (d - L0) * (r / d) - Kd * VD * (r/d)
    return Fs

def SommeForce(j):
    F = [0, 0]
    if P[j].Mouse != []:
        F += ForceRessort('MousePoint',j, springMouse)
    for i in P[j].L:
        F += ForceRessort(i, j, springVoi)

    for i in P[j].L2:
        F += ForceRessort(i, j, springHor)
    
    F[1]+=P[j].m * gravite
    return F

Points = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
Points = []
for i in range(30):
    if i%5 == 0:
        Points.append([])
    Points[-1].append(i)
        
# Points = [[0,1], [2, 3]]
#Points = [[0]]
P = {'MousePoint':point()}
for i in Points:
    for x in i:
        P[x] = point()
        
springMouse = Spring()
springMouse.Ks = 50
springMouse.L0 = 0
springVoi = Spring()
springHor = Spring()
springHor.Ks = 15
springHor.L0 = math.sqrt(2*(springVoi.L0**2))

alpha = 0.1
collisionBox = 5
PositionDepart = 300
Espacement = 30
gravite = 2
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
        P[point].vx = (P[point].vx*-1) / 4
    if y+collisionBox >= height:
        P[point].y = height-collisionBox
        P[point].vy = (P[point].vy*-1) / 4
    if x <= 0:
        P[point].x = 0
        P[point].vx = (P[point].vx*-1) / 4
    if y <= 0:
        P[point].y = 0
        P[point].vy = (P[point].vy*-1) / 4
Init()

nbr = 0
def actu(nbr):
    nbr+=1
    can.delete('all')
    dt = 0.1
    if clicked:
        minDis = 100
        po = 0
        for i in Points:
            for x in i:
                P[x].Mouse = []
                dis = abs(math.sqrt((P[x].x - P['MousePoint'].x)**2 + (P[x].y - P['MousePoint'].y)**2))
                if dis < minDis:
                    minDis = dis
                    po = x
        
        P[po].Mouse = [0,0]
        P[po].Mouse[0], P[po].Mouse[1] = P['MousePoint'].x, P['MousePoint'].y
        can.create_line(P[po].x, P[po].y, P['MousePoint'].x, P['MousePoint'].y, fill = 'white')
    else:
        P[0].Mouse = []
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
    window.after(1, actu, nbr)

import tkinter as tk
clicked = False

def click(event):
    global clicked
    P['MousePoint'].x, P['MousePoint'].y = event.x, event.y
    clicked = True

def unclick(event):
    global clicked
    for i in Points:
        for x in i:
            P[x].Mouse = []
    clicked = False

def motion(event):
    if clicked:
        P['MousePoint'].x, P['MousePoint'].y = event.x, event.y
window = tk.Tk()
window.title('softBody')

can = tk.Canvas(window, bg = '#192332', width = width, height = height)
can.grid()
can.bind('<Button>', click)
can.bind('<ButtonRelease>', unclick)
can.bind('<Motion>', motion)

window.after(2000, actu, nbr)

window.mainloop()