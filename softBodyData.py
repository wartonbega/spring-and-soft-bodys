import time
import tkinter as tk
import math as m
class MassPoint():
    def __init__(self):
        self.x = 1
        self.v = 0
        self.F = 0
        self.m = 5

    def Update(self, Dt):
#        self.F += self.m * -9.81
        self.v += self.F * Dt / self.m
        self.x += self.v * Dt

        
class Spring():
    def __init__(self):
        self.A, self.B = Points['1'], Points['2']
        self.Ks = 1
        self.L0 = 10
        self.Kd = 5
    
    def HooksLaw(self):
        self.A.F = 0
        self.B.F = 0
        A = self.A.x
        B = self.B.x
        Fs = self.Ks * abs(B - A) - self.L0
        Fd = ((B - A) / abs(B - A)) * (self.B.v - self.A.v) * self.Kd
        Ft = Fs + Fd
        Fa = Ft * ((B - A)/abs(B - A))
        Fb = Ft * ((A - B)/abs(A - B))
        self.A.F += Fa
        self.B.F += Fb  
        
        
Points = {'1' : MassPoint(), '2': MassPoint(), '3': MassPoint()}
Points['2'].x = 50
Points['2'].m = 5
Points['3'].x = 70

spring = Spring()
spring2 = Spring()
spring2.A = Points['2']
spring2.B = Points['3']
spring2.L0 = 50

#spring3 = Spring()
#spring3.A = Points['1']
#spring3.B = Points['3']

window = tk.Tk()
window.config(bg = '#192332')
def chute():
    can.delete('all')
    spring.HooksLaw()
#    spring2.HooksLaw()
#    spring3.HooksLaw()
    for point in range(1, 3):
        Points[str(point)].Update(0.1)
        x = Points[str(point)].x
        can.create_rectangle(100+x, 100+x, 100+x+2, 100+x+2, fill = 'red', outline = 'red')
        
    can.create_line(100+Points['1'].x, 100+Points['1'].x, 100+Points['2'].x, 100+Points['2'].x, fill = 'white')
    window.after(10, chute)

Ks = tk.LabelFrame(window, text="Constante de raideur", padx=20, pady=20, bg = '#192332', fg = 'white')
Ks.grid(row = 1, column = 2)

L0 = tk.LabelFrame(window, text="Longueure au repos", padx=20, pady=20, bg = '#192332', fg = 'white')
L0.grid(row = 1, column = 0)

can = tk.Canvas(window)
can.config(bg = '#192332')
can.grid(row = 0, column = 1) 

def ChangeL0(event):
    value = scale.get()
    spring.L0 = int(value)

def ChangeKs(event):
    value = scale2.get()
    spring.Ks = value

value = spring.L0
value2 = spring.Ks
scale = tk.Scale(L0, variable=value, command = ChangeL0, bg = '#192332', fg = 'white')
scale.grid(row = 0, column = 0)

scale2 = tk.Scale(Ks, variable=value2, command = ChangeKs, bg = '#192332', fg = 'white')
scale2.grid(row = 0, column = 2)

window.after(10, chute)


window.mainloop()