
############################################################################### Library Import ########

import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import Point
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

############################################################################### Library Import ########


################################################################ MAIN PROGRAM #############################

bmap=0
bound=0
sc=0
path=0
x,y=77.5031,28.67535
info={1:'CS_IT',2:'main_block',3:'back_block',4:'faith_centre',5:'mca_block',6:'me_block',7:'skill_centre',8:'tifac_core',9:'mechanical_canteen',10:'workshop',11:'professors_parking',12:'lecture_theater'}
def read_building_data():
    global BBox
    global akgec
    global data
    global path_data
    
    data =[]
    path_data=[]
    
    for i in range(0,12):
        data.append(pd.read_csv('buildings_data\\'+ str(i+1) + '.txt' ))

    for i in range(0,22):
        path_data.append(pd.read_csv('buildings_data\\'+ 'p' +str(i+1) + '.txt' ))
    
                                
    BBox = (77.49906,77.50562,28.67309, 28.67793)
    akgec = plt.imread('buildings_data\map.png')
    
def plot():
    global fig
    global ax
    global BBox
    fig, ax = plt.subplots(figsize = (8,8))
    ax.axis('off')
    ax.set_title('Plotting Spatial Data on AKGEC Map')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    
def base_map():
    global akg
    global akgec
    global ax
    global bmap
    global canves
    if bmap == 1:
        akg.remove()
        bmap=0
        canves.draw()
    else:
        akg = ax.imshow(akgec, zorder=0, extent = BBox, aspect= 'equal')
        bmap=1
        canves.draw()
def boundaries():
    global data
    global ax
    global Bound
    global bound
    global canves
    global figures
    
    if bound == 1:
        bound=0
        for i in Bound:
            i.remove()
        canves.draw()
    else:
        Bound = []
        figures = []
        for i in data:
            draw=Polygon(np.column_stack((np.array(i.longitude),np.array(i.latitude))))
            figures.append(draw)
            x,y=draw.exterior.xy
            a,=ax.plot(x,y, color='#6699cc', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
            Bound.append(a)
        bound = 1
        canves.draw()

def scatter():
    global data
    global ax
    global sc
    global Sc
    global canves
    if sc ==1:
        for i in Sc:
            i.remove()
        sc=0
        canves.draw()
    else:
        Sc=[]
        for i in data:
            a= ax.scatter(i.longitude, i.latitude, zorder=1, alpha= 0.2, c='b', s=30)
            Sc.append(a)
        sc=1
        canves.draw()
def path_draw():
    global path_data
    global ax
    global Path
    global path
    global canves
    
    if path == 1:
        for i in Path:
            i.remove()
        canves.draw()
        path=0
    else:
        Path=[]
        for i in path_data:
            a,=ax.plot(i.longitude,i.latitude, color='#FF0000',zorder=2)
            Path.append(a)
        path=1
        canves.draw()

############################################################## INIT ###########
        
read_building_data()
plot()

############################################################## INIT ###########

#################################### GUI ####################################################

root= tk.Tk()

########################################################### Tkinter Canves ####

canves = FigureCanvasTkAgg(fig, root)
canves.get_tk_widget().place(relx=0.5,rely=0.5,anchor=W)
canves.get_tk_widget().grid(row=1,column=1,columnspan=5,rowspan=20,sticky=NSEW)

########################################################### Tkinter Canves ##################

base_map()
boundaries()

pos = ax.scatter(x,y)

b1= Button(root,text="Base Map",  command = base_map)
b1.grid(row=1,column=6)
b2= Button(root,text="Boundaries", command = boundaries)
b2.grid(row=2,column=6)
b3= Button(root,text="scatter", command = scatter)
b3.grid(row=3,column=6)
b3= Button(root,text="Path",  command = path_draw)
b3.grid(row=4,column=6)

def key(event):
    global x
    global y
    global ax
    global canves
    global pos
    global info
    pos.remove()
    c= str(repr(event.char))
    if c[1] == 'w':
        y=y+0.000028
    elif c[1] == 's':
        y=y-0.000028
    elif c[1] == 'a':
        x=x-0.000028
    elif c[1] == 'd':
        x=x+0.000028
    pos = ax.scatter(x,y)
    p=Point(x,y)
    for i in range(0,len(figures)):
        if figures[i].contains(p):
            ax.set_title("Inside " + info[i+1])
            break
    else:
        ax.set_title("Inside AKGEC")
    canves.draw()

def callback(event):
    frame.focus_set()
    print ("clicked at", event.x, event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.grid(row=5,column=6)
#plt.show()

root.mainloop()

################################## GUI ########################################



################################################################ MAIN PROGRAM #############################
