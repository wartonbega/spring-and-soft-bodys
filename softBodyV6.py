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
    VD = (VV[0] * r[0] + VV[1] * r[1]) / d # Projection de VV
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
for i in range(40):
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


alpha = 0.1
collisionBox = 2
PositionDepart = 200
Espacement = 40
gravite = 2
width = 700
height = 450
absorption = 10

springVoi.L0 = Espacement
springHor.L0 = math.sqrt(2*(springVoi.L0**2))

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
        P[point].vx = (P[point].vx*-1) / absorption
    if y+collisionBox >= height:
        P[point].y = height-collisionBox
        P[point].vy = (P[point].vy*-1) / absorption
    if x <= 0:
        P[point].x = 0
        P[point].vx = (P[point].vx*-1) / absorption
    if y <= 0:
        P[point].y = 0
        P[point].vy = (P[point].vy*-1) / absorption
Init()

nbr = 0
def actu(nbr):
    global timeSelected
    nbr+=1
    can.delete('all')
    dt = 0.1
    if clicked:
        P['MousePoint'].L0 = 0
        minDis = np.inf
        po = 0
        for i in Points:
            for x in i:
                P[x].Mouse = []
                dis = abs(math.sqrt((P[x].x - P['MousePoint'].x)**2 + (P[x].y - P['MousePoint'].y)**2))
                if dis < minDis:
                    minDis = dis
                    po = x
        if mouseBehaviour == 'Ressort':
            P[po].Mouse = [0,0]
            P[po].Mouse[0], P[po].Mouse[1] = P['MousePoint'].x, P['MousePoint'].y
            can.create_line(P[po].x, P[po].y, P['MousePoint'].x, P['MousePoint'].y, fill = 'white')
        elif mouseBehaviour == '"Attrapage"':
            P[po].x, P[po].y = P['MousePoint'].x,P['MousePoint'].y
    else:
        P[0].Mouse = []
    for i in Points:
        for x in i:
            vx, vy = P[x].vx, P[x].vy
            m = P[x].m
            F = SommeForce(x)
            P[x].dx = vx * dt * float(timeSelected)
            P[x].dy = vy * dt * float(timeSelected)
            P[x].dvx = 1/m * F[0] * dt * float(timeSelected)
            P[x].dvy = 1/m * F[1] * dt * float(timeSelected)

            
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
repuslif = True

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
        
def changeGravity():
    global gravite
    gravite = float(GraviteSpinBox.get())
    
def changeL0():
    springVoi.L0 = int(L0SpinBox.get())
    springHor.L0 = math.sqrt(2 * springVoi.L0**2)

def changeKs():
    springVoi.Ks = int(KsSpinBox.get())
    springHor.Ks = int(KsSpinBox.get())

def changeKd():
    springVoi.Kd = int(KsSpinBox.get())
    springHor.Kd = int(KsSpinBox.get())

def changeM():
    for i in Points:
        for x in i:
            P[x].m = int(MSpinBox.get())

def timeSelect():
    global timeSelected
    timeSelected = TimeMult.get()

def ChangeMouseBehaviour():
    global mouseBehaviour
    mouseBehaviour = str(MouseBe.get())

mouseBehaviour = 'Ressort'
timeSelected = 1

window = tk.Tk()
window.title('softBody')
window.config(bg = '#2a2a2e')

LabelGravite = tk.LabelFrame(window, text = 'Constante de gravité', bg = '#2a2a2e', fg = 'white', )
LabelGravite.grid(column = 0, row = 1)
GraviteSpinBox = tk.Spinbox(LabelGravite, from_ = 0, to_ = 10, command = changeGravity, bg = '#2a2a2e', fg = 'white', wrap = True)
GraviteSpinBox.pack()
GraviteSpinBox.delete(0, tk.END)
GraviteSpinBox.insert(tk.END, str(gravite))
#2a2a2e
LabelL0 = tk.LabelFrame(window, text = 'Longueure au repos', bg = '#2a2a2e', fg = 'white')
LabelL0.grid(column = 0, row = 2)
L0SpinBox = tk.Spinbox(LabelL0, from_ = 10, to_ = 50, command = changeL0,bg = '#2a2a2e', fg = 'white', wrap = True)
L0SpinBox.pack()
L0SpinBox.delete(0, tk.END)
L0SpinBox.insert(tk.END, str(springVoi.L0))

LabelKs = tk.LabelFrame(window, text = "Constante de d'élasticitée", bg = '#2a2a2e', fg = 'white')
LabelKs.grid(column = 0, row = 3)
KsSpinBox = tk.Spinbox(LabelKs, from_ = 5, to_ = 100, command = changeKs,bg = '#2a2a2e', fg = 'white', wrap = True)
KsSpinBox.pack()
KsSpinBox.delete(0, tk.END)
KsSpinBox.insert(tk.END, str(springVoi.Ks))

LabelKd = tk.LabelFrame(window, text = "Constante de de frottement", bg = '#2a2a2e', fg = 'white')
LabelKd.grid(column = 0, row = 4)
KdSpinBox = tk.Spinbox(LabelKd, from_ = 5, to_ = 100, command = changeKd,bg = '#2a2a2e', fg = 'white', wrap = True)
KdSpinBox.pack()
KdSpinBox.delete(0, tk.END)
KdSpinBox.insert(tk.END, str(springVoi.Kd))

LabelM = tk.LabelFrame(window, text = 'Masse des points', bg = '#2a2a2e', fg = 'white')
LabelM.grid(column = 0, row = 5)
MSpinBox = tk.Spinbox(LabelM, from_ = 5, to_ = 50, command = changeM,bg = '#2a2a2e', fg = 'white', wrap = True)
MSpinBox.pack()
MSpinBox.delete(0, tk.END)
MSpinBox.insert(tk.END, str(P[0].m))

var = f'''La souris permet d'atirer l'objet vers un point.
Recommendation : ne pas faire tourner l'objet sur lui même\n quand il n'y as pas de gravitée.
'''
Label = tk.Label(window, text = var, bg = '#2a2a2e', fg = 'white')
Label.grid(column = 0, row = 6)

can = tk.Canvas(window, bg = '#192332', width = width, height = height, highlightthickness=1)
can.grid(column = 0, row = 0)
can.bind('<Button>', click)
can.bind('<ButtonRelease>', unclick)
can.bind('<Motion>', motion)


LabelTemps = tk.LabelFrame(window, text = 'Vitesse de la simulation', bg = '#2a2a2e', fg = 'white')
LabelTemps.grid(column = 1, row = 0)
TimeMult = tk.Spinbox(LabelTemps, values=[0.0625, 0.125,0.25,0.5,1,1.5], command = timeSelect, bg = '#2a2a2e', fg = 'white')
TimeMult.grid(column =1, row=0)
TimeMult.delete(0, tk.END)
TimeMult.insert(tk.END, str(1))


LabelMouse = tk.LabelFrame(window, text = "Type d'interaction de la souris", bg = '#2a2a2e', fg = 'white')
LabelMouse.grid(column = 1, row = 1)
MouseBe = tk.Spinbox(LabelMouse, values=['Ressort','"Attrapage"'], command = ChangeMouseBehaviour, bg = '#2a2a2e', fg = 'white')
MouseBe.grid(column =1, row=1)

window.after(2000, actu, nbr)

window.mainloop()
