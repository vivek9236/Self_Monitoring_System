import tkinter as tk 
from tkinter import ttk 
from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import Point
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import time
from datetime import date
import random
import mplcursors
import math
import speech_recognition as sr

LARGEFONT =("Segoe Script", 35)
BFONT=("Comic Sans MS", 8)
TFONT=("Comic Sans MS", 12)
conn = sqlite3.connect('Profile.db')
c = conn.cursor()
conn1 = sqlite3.connect('tvar_data.db')
c1 = conn1.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS settings
             (id integer PRIMARY KEY,refresh integer,unit text,b_color text,e_color text,l_color text);''')
c.execute("SELECT * FROM settings")
r=c.fetchall()
if(len(r)== 0):
        r=[[1,5,'Sec','blue','red','green']]
c.execute('''CREATE TABLE IF NOT EXISTS profile
             (id integer PRIMARY KEY,fname text, mname text, lname text, branch text, section text, snumber integer, rnumber integer, gender integer, email text);''')
c.execute("SELECT * FROM profile")
r1=c.fetchall()
if(len(r1) == 0):
        r1=[[1,'','','','','',0,0,0,'']]
e=0
ti=r[0][1]
units=r[0][2]
if r[0][3] == 'Random (try it)':
        b_color=[random.choice(['red','blue','green','pink','yellow','brown','cyan']) for i in range(0,17)]
else:
        b_color=[r[0][3] for i in range(0,17)]

e_color=r[0][4]
l_color=r[0][5]
nav=''

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        
        self.lb_up = False

    def changed(self, name, index, mode):
            
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        global nav

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
            nav=self.var.get()


    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


class SMSApp(tk.Tk):

        def close_window(self):
                #print("Window closed")
                t=str(date.today()).split('-')
                global c1
                global conn1
                global conn
                c1.execute('''CREATE TABLE IF NOT EXISTS current
             (day integer PRIMARY KEY,a0 integer,a1 integer,a2 integer,a3 integer,a4 integer,a5 integer,a6 integer,a7 integer,a8 integer,a9 integer,a10 integer,a11 integer,a12 integer,a13 integer,a14 integer,a15 integer,a16 integer,a17 integer,a18 integer,a19 integer);''')
                conn1.commit()
                c1.execute("SELECT * FROM current")
                rows=c1.fetchall()
                #print(t[2])
                if(len(rows)== 0):
                        rows=[[0]]
                if(len(rows)!=0 and t[2] == str(rows[len(rows)-1][0])):
                        #print(0)
                        c1.execute("DELETE FROM current WHERE day ="+str(t[2]))
                        c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(t[2],rows[len(rows)-1][1]+self.frames[StartPage].tvar_data[0],rows[len(rows)-1][2]+self.frames[StartPage].tvar_data[1],rows[len(rows)-1][3]+self.frames[StartPage].tvar_data[2],rows[len(rows)-1][4]+self.frames[StartPage].tvar_data[3],rows[len(rows)-1][5]+self.frames[StartPage].tvar_data[4],rows[len(rows)-1][6]+self.frames[StartPage].tvar_data[5],rows[len(rows)-1][7]+self.frames[StartPage].tvar_data[6],rows[len(rows)-1][8]+self.frames[StartPage].tvar_data[7],rows[len(rows)-1][9]+self.frames[StartPage].tvar_data[8],rows[len(rows)-1][10]+self.frames[StartPage].tvar_data[9],rows[len(rows)-1][11]+self.frames[StartPage].tvar_data[10],rows[len(rows)-1][12]+self.frames[StartPage].tvar_data[11],rows[len(rows)-1][13]+self.frames[StartPage].tvar_data[12],rows[len(rows)-1][14]+self.frames[StartPage].tvar_data[13],rows[len(rows)-1][15]+self.frames[StartPage].tvar_data[14],rows[len(rows)-1][16]+self.frames[StartPage].tvar_data[15],rows[len(rows)-1][17]+self.frames[StartPage].tvar_data[16],rows[len(rows)-1][18]+self.frames[StartPage].tvar_data[17],rows[len(rows)-1][19]+self.frames[StartPage].tvar_data[18],rows[len(rows)-1][20]+self.frames[StartPage].tvar_data[19]))
                else:
                        #print(1)
                        for i in range(1,int(t[2])-rows[len(rows)-1][0]):
                                c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(rows[len(rows)-1][0]+i,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
                        c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(t[2],self.frames[StartPage].tvar_data[0],self.frames[StartPage].tvar_data[1],self.frames[StartPage].tvar_data[2],self.frames[StartPage].tvar_data[3],self.frames[StartPage].tvar_data[4],self.frames[StartPage].tvar_data[5],self.frames[StartPage].tvar_data[6],self.frames[StartPage].tvar_data[7],self.frames[StartPage].tvar_data[8],self.frames[StartPage].tvar_data[9],self.frames[StartPage].tvar_data[10],self.frames[StartPage].tvar_data[11],self.frames[StartPage].tvar_data[12],self.frames[StartPage].tvar_data[13],self.frames[StartPage].tvar_data[14],self.frames[StartPage].tvar_data[15],self.frames[StartPage].tvar_data[16],self.frames[StartPage].tvar_data[17],self.frames[StartPage].tvar_data[18],self.frames[StartPage].tvar_data[19]))
                 
                conn1.commit()
                c1.execute("SELECT * FROM current")
                rows=c1.fetchall()
                conn1.close()
                conn.close()
                print(self.frames[StartPage].tvar_data)
                print(rows)
                
                self.destroy()
                
        def __init__(self, *args, **kwargs):

                global r1
                
                tk.Tk.__init__(self, *args, **kwargs)
                self.protocol("WM_DELETE_WINDOW", self.close_window)
                container = tk.Frame(self)
                container.pack(side = "top", fill = "both", expand = True) 
                container.grid_rowconfigure(0, weight = 1) 
                container.grid_columnconfigure(0, weight = 1)
                self.title("Self Monitoring System - " + r1[0][1])
                ws = self.winfo_screenwidth()
                x = (ws/7)
                y = 0
                self.geometry('+%d+%d' % (x, y))

                self.frames = {} 
 
                for F in (StartPage, Profile, Settings,Visualize): 

                        frame = F(container, self) 

                        self.frames[F] = frame 

                        frame.grid(row = 0, column = 0, sticky ="nsew") 

                self.show_frame(StartPage) 
 
        def show_frame(self, cont): 
                frame = self.frames[cont] 
                frame.tkraise()


class StartPage(tk.Frame):
    bmap=0
    bound=0
    sc=0
    path=0
    x,y=77.5031,28.67535
    info={1:'CS/IT Block',2:'Main Block',3:'Back Block',4:'Faith Centre',5:'MCA Block',6:'Mechanical Block',7:'Skill Centre',8:'Tiffac Core',9:'Mechanical Canteen',10:'Workshop',11:'Professors Parking',12:'Lecture Theaters',13:'Girls Hostel 1',14:'Girls Hostel 2',15:'Parking',16:'Girls Hostel 3',17:'senior boys hostel',18:'Boys Hostel 2',19:'Boys Hostel 3'}
    BBox = (77.49906,77.50562,28.67309, 28.67793)
    cur=0
    tvar_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pa=[None,None,None]

    def calcEdgeLen(a,b):
            all_nodes = pd.read_csv('route.txt')
            sno_vect = np.array(all_nodes.sno).tolist()
            lats_vect = np.array(all_nodes.latitude).tolist()
            lons_vect = np.array(all_nodes.longitude).tolist()
            x1, y1=lons_vect[a], lats_vect[a]
            x2, y2=lons_vect[b], lats_vect[b]
            edge_len = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return edge_len 

    graph = {
    0:{1:calcEdgeLen(0,1)},
    1:{0:calcEdgeLen(0,1), 2:calcEdgeLen(1,2), 87:calcEdgeLen(87,1),},
    2:{1:calcEdgeLen(1,2), 3:calcEdgeLen(2,3), 19:calcEdgeLen(2,19)},
    3:{2:calcEdgeLen(2,3), 4:calcEdgeLen(3,4)},
    4:{3:calcEdgeLen(3,4), 5:calcEdgeLen(4,5)},
    5:{4:calcEdgeLen(4,5), 6:calcEdgeLen(5,6), 80:calcEdgeLen(80,5)},
    6:{5:calcEdgeLen(5,6), 7:calcEdgeLen(6,7), 20:calcEdgeLen(6,20)},
    7:{6:calcEdgeLen(6,7), 8:calcEdgeLen(7,8)},
    8:{7:calcEdgeLen(7,8), 9:calcEdgeLen(8,9), 23:calcEdgeLen(8,23)},
    9:{8:calcEdgeLen(8,9), 10:calcEdgeLen(9,10)},
    10:{9:calcEdgeLen(9,10),11:calcEdgeLen(10,11)},
    11:{10:calcEdgeLen(10,11), 12:calcEdgeLen(11,12), 46:calcEdgeLen(11,46)},
    12:{11:calcEdgeLen(11,12), 13:calcEdgeLen(12,13)},
    13:{12:calcEdgeLen(12,13), 14:calcEdgeLen(13,14), 64:calcEdgeLen(13,64)},
    14:{13:calcEdgeLen(13,14), 15:calcEdgeLen(14,15)},
    15:{14:calcEdgeLen(14,15), 16:calcEdgeLen(15,16), 71:calcEdgeLen(15,71)},
    16:{15:calcEdgeLen(15,16), 17:calcEdgeLen(16,17)},
    17:{16:calcEdgeLen(16,17)},
    18:{4:calcEdgeLen(4,18), 19:calcEdgeLen(18,19)},
    19:{2:calcEdgeLen(2,19), 18:calcEdgeLen(18,19)},
    20:{6:calcEdgeLen(6,20), 21:calcEdgeLen(20,21), 24:calcEdgeLen(20,24)},
    21:{20:calcEdgeLen(20,21), 22:calcEdgeLen(21,22)},
    22:{21:calcEdgeLen(21,22), 23:calcEdgeLen(22,23), 29:calcEdgeLen(22,29)},
    23:{22:calcEdgeLen(22,23), 8:calcEdgeLen(8,23), 45:calcEdgeLen(23,45)},
    24:{20:calcEdgeLen(20,24), 25:calcEdgeLen(24,25), 40:calcEdgeLen(24,40)},
    25:{24:calcEdgeLen(24,25), 26:calcEdgeLen(25,26)},
    26:{25:calcEdgeLen(25,26), 27:calcEdgeLen(26,27)},
    27:{26:calcEdgeLen(26,27), 28:calcEdgeLen(27,28)},
    28:{27:calcEdgeLen(27,28)},
    29:{22:calcEdgeLen(22,29), 30:calcEdgeLen(29,30)},
    30:{29:calcEdgeLen(29,30), 31:calcEdgeLen(30,31)},
    31:{30:calcEdgeLen(30,31), 32:calcEdgeLen(31,32)},
    32:{31:calcEdgeLen(31,32), 33:calcEdgeLen(32,33), 76:calcEdgeLen(32,76)},
    33:{32:calcEdgeLen(32,33), 34:calcEdgeLen(33,34)},
    34:{33:calcEdgeLen(33,34), 35:calcEdgeLen(34,35)},
    35:{34:calcEdgeLen(34,35), 36:calcEdgeLen(35,36)},
    36:{35:calcEdgeLen(35,36), 37:calcEdgeLen(36,37)},
    37:{36:calcEdgeLen(36,37), 38:calcEdgeLen(37,38)},
    38:{37:calcEdgeLen(37,38), 39:calcEdgeLen(38,39)},
    39:{38:calcEdgeLen(38,39)},
    40:{24:calcEdgeLen(24,40), 41:calcEdgeLen(40,41)},
    41:{40:calcEdgeLen(40,41), 42:calcEdgeLen(41,42)},
    42:{41:calcEdgeLen(41,42), 43:calcEdgeLen(42,43)},
    43:{42:calcEdgeLen(42,43), 44:calcEdgeLen(43,44)},
    44:{43:calcEdgeLen(43,44), 21:calcEdgeLen(21,44)},
    45:{23:calcEdgeLen(23,45), 46:calcEdgeLen(45,46)},
    46:{11:calcEdgeLen(11,46), 45:calcEdgeLen(45,46), 47:calcEdgeLen(46,47)},
    47:{48:calcEdgeLen(47,48), 46:calcEdgeLen(46,47), 63:calcEdgeLen(47,63)},
    48:{47:calcEdgeLen(47,48), 49:calcEdgeLen(48,49), 55:calcEdgeLen(48,55)},
    49:{48:calcEdgeLen(48,49), 50:calcEdgeLen(49,50)},
    50:{49:calcEdgeLen(49,50), 51:calcEdgeLen(50,51)},
    51:{50:calcEdgeLen(50,51), 52:calcEdgeLen(51,52), 58:calcEdgeLen(51,58)},
    52:{51:calcEdgeLen(51,52), 53:calcEdgeLen(52,53), 56:calcEdgeLen(52,56)},
    53:{52:calcEdgeLen(52,53), 54:calcEdgeLen(53,53)},
    54:{53:calcEdgeLen(53,54)},
    55:{48:calcEdgeLen(48,55), 74:calcEdgeLen(74,55)},
    56:{52:calcEdgeLen(52,56), 57:calcEdgeLen(56,57)},
    57:{56:calcEdgeLen(56,57), 58:calcEdgeLen(57,58)},
    58:{57:calcEdgeLen(57,58), 51:calcEdgeLen(51,58)},
    59:{60:calcEdgeLen(59,60), 65:calcEdgeLen(59,65), 66:calcEdgeLen(59,66)},
    60:{59:calcEdgeLen(59,60), 61:calcEdgeLen(60,61)},
    61:{60:calcEdgeLen(60,61), 62:calcEdgeLen(61,62), 63:calcEdgeLen(61,63)},
    62:{61:calcEdgeLen(61,62)},
    63:{47:calcEdgeLen(47,63), 61:calcEdgeLen(61,63)},
    64:{13:calcEdgeLen(13,64), 65:calcEdgeLen(64,65)},
    65:{64:calcEdgeLen(64,65), 59:calcEdgeLen(59,65)},
    66:{59:calcEdgeLen(59,66), 70:calcEdgeLen(66,70), 67:calcEdgeLen(67,66)},
    67:{66:calcEdgeLen(66,67), 68:calcEdgeLen(67,68), 69:calcEdgeLen(67,69)},
    68:{67:calcEdgeLen(67,68)},
    69:{67:calcEdgeLen(67,69)},
    70:{66:calcEdgeLen(66,70)},
    71:{15:calcEdgeLen(15,71), 72:calcEdgeLen(71,72)},
    72:{71:calcEdgeLen(71,72), 73:calcEdgeLen(72,73)},
    73:{72:calcEdgeLen(72,73)},
    74:{55:calcEdgeLen(55,74), 75:calcEdgeLen(74,75)},
    75:{74:calcEdgeLen(74,75)},
    76:{32:calcEdgeLen(32,76), 77:calcEdgeLen(76,77)},
    77:{76:calcEdgeLen(76,77), 78:calcEdgeLen(77,78)},
    78:{77:calcEdgeLen(77,78), 79:calcEdgeLen(78,79)},
    79:{78:calcEdgeLen(78,79)},
    80:{81:calcEdgeLen(80,81), 5:calcEdgeLen(5,80), 89:calcEdgeLen(89,80)},
    81:{82:calcEdgeLen(81,82), 80:calcEdgeLen(80,81), 92:calcEdgeLen(81,92)},
    82:{83:calcEdgeLen(82,83), 81:calcEdgeLen(81,82)},
    83:{84:calcEdgeLen(83,84), 88:calcEdgeLen(83,88), 82:calcEdgeLen(82,83)},
    84:{85:calcEdgeLen(84,85), 83:calcEdgeLen(83,84)},
    85:{86:calcEdgeLen(85,86), 84:calcEdgeLen(84,85), 90:calcEdgeLen(90,85)},
    86:{87:calcEdgeLen(86,87), 85:calcEdgeLen(85,86)},
    87:{1:calcEdgeLen(1,87), 91:calcEdgeLen(87,91), 86:calcEdgeLen(87,86)},
    88:{83:calcEdgeLen(83,88), 89:calcEdgeLen(88,89), 90:calcEdgeLen(90,88)},
    89:{80:calcEdgeLen(80,89), 88:calcEdgeLen(88,89)},
    90:{85:calcEdgeLen(85,90), 88:calcEdgeLen(88,90)},
    91:{87:calcEdgeLen(87,91)},
    92:{81:calcEdgeLen(81,92), 93:calcEdgeLen(92,93)},
    93:{92:calcEdgeLen(92,93), 94:calcEdgeLen(93,94)},
    94:{93:calcEdgeLen(93,94), 95:calcEdgeLen(94,95)},
    95:{94:calcEdgeLen(94,95), 96:calcEdgeLen(95,96)},
    96:{95:calcEdgeLen(95,96), 97:calcEdgeLen(97,96)},
    97:{96:calcEdgeLen(96,97), 98:calcEdgeLen(97,98)},
    98:{97:calcEdgeLen(97,98)},
    }

    def plot_path_data(self,ax,canves,path):

        if(self.pa[0] != None):
                self.pa[0].remove()
                self.pa[1].remove()
                self.pa[2].remove()
                canves.draw()

        plt.style.use("fivethirtyeight")

        path_data = pd.read_csv('route.txt')

        la=[]
        lo=[]
        for i in range(len(path)):
            la.append(np.array(path_data[path_data.sno == path[i]].latitude).tolist()[0])
            lo.append(np.array(path_data[path_data.sno == path[i]].longitude).tolist()[0])

        self.pa[0],=ax.plot(lo,la,color='#8f1021', linestyle='solid', marker='o',markerfacecolor='#f7f36a', markersize=5, label='Shortest Path Route between S and D')
        self.pa[1],=ax.plot(lo[0],la[0],marker="o",markerfacecolor='#39f7ee', markersize=10, label='Source(S)')
        self.pa[2],=ax.plot(lo[len(lo)-1],la[len(la)-1],marker="o",markerfacecolor='#f7170f', markersize=10, label='Destination(D)')
        canves.draw()

    def shortestPath(self,ax,canves,d):
        unvisited_nodes = {}
        for i in self.graph.keys():
                unvisited_nodes[i]=self.graph[i]
        da=pd.read_csv('route.txt')
        a=list(da.longitude)
        b=list(da.latitude)
        points=[]
        for i in range(len(a)):
            points.append([a[i]-self.x,b[i]-self.y])
            
        K=1
        points.sort(key = lambda K: K[0]**2 + K[1]**2)

        source=list(da[da.longitude == (points[:K][0][0]+self.x)].sno)[0]
        destination=d

        min_distance = {}
        predecessor = {}

        huge_number = 99999999
        path = []

        for node in unvisited_nodes:
            if node == source:
                min_distance[source] = 0
            else:
                min_distance[node] = huge_number

        while unvisited_nodes:
            min_distance_node = None

            for node in unvisited_nodes:
                if min_distance_node is None:
                    min_distance_node = node

                elif min_distance[node] < min_distance[min_distance_node]:
                    min_distance_node = node

            child_paths = self.graph[min_distance_node].items()

            for child_node, cost in child_paths:

                if cost + min_distance[min_distance_node] < min_distance[child_node]:

                    min_distance[child_node] = cost + min_distance[min_distance_node]

                    predecessor[child_node] = min_distance_node

            unvisited_nodes.pop(min_distance_node)

        ptr = destination

        while ptr != source:

            try:
                path.insert(0,ptr)
                ptr = predecessor[ptr]
            except KeyError:
                print("Path can't be reached")
                break

        path.insert(0,source)

        if min_distance[destination] != huge_number:
                self.plot_path_data(ax,canves,path)

    
    def read_building_data(self):
        
        self.data =[]
        self.path_data=[]
        
        for i in range(0,19):
            self.data.append(pd.read_csv('buildings_data\\'+ str(i+1) + '.txt' ))

        for i in range(0,22):
            self.path_data.append(pd.read_csv('buildings_data\\'+ 'p' +str(i+1) + '.txt' ))
        
        self.akgec = plt.imread('buildings_data\map.png')
    def plot(self):
        self.fig, self.ax = plt.subplots(figsize = (9,7))
        self.ax.axis('off')
        self.ax.set_title('Plotting Spatial Data on AKGEC Map')
        self.ax.set_xlim(self.BBox[0],self.BBox[1])
        self.ax.set_ylim(self.BBox[2],self.BBox[3])
    def base_map(self):
        if self.bmap == 1:
            self.akg.remove()
            self.bmap=0
            self.canves.draw()
        else:
            self.akg = self.ax.imshow(self.akgec, zorder=0, extent = self.BBox, aspect= 'equal')
            self.bmap=1
            self.canves.draw()
    def boundaries(self):
        
        if self.bound == 1:
            self.bound=0
            for i in self.Bound:
                i.remove()
            self.canves.draw()
        else:
            self.Bound = []
            self.figures = []
            for i in self.data:
                draw=Polygon(np.column_stack((np.array(i.longitude),np.array(i.latitude))))
                self.figures.append(draw)
                x,y=draw.exterior.xy
                a,=self.ax.plot(x,y, color='#6699cc', alpha=0.7,linewidth=3, solid_capstyle='round', zorder=2)
                self.Bound.append(a)
            self.bound = 1
            self.canves.draw()

    def scatter(self):
        self.ax.scatter(77.50326170000001,28.6752174, zorder=1, alpha= 0.2, c='b', s=30)
        if self.sc ==1:
            for i in self.Sc:
                i.remove()
            self.sc=0
            self.canves.draw()
        else:
            self.Sc=[]
            for i in self.data:
                a= self.ax.scatter(i.longitude, i.latitude, zorder=1, alpha= 0.2, c='b', s=30)
                self.Sc.append(a)
            self.sc=1
            self.canves.draw()

    def path_draw(self):
    
        if self.path == 1:
            for i in self.Path:
                i.remove()
            self.canves.draw()
            self.path=0
        else:
            self.Path=[]
            
            for i in self.path_data:
                a,=self.ax.plot(i.longitude,i.latitude, color='#FF0000',zorder=2)
                self.Path.append(a)
            self.path=1
            self.canves.draw()
    def showtime(self):
        global e
        global timer
        global c1
        global conn1
        seconds = time.time()
        t = time.ctime(seconds)
        self.v.set(t)
        t=str(date.today()).split('-')
        self.tvar_data[self.cur]=self.tvar_data[self.cur]+1
        e=e+1
        #print(self.tvar_data)
        
        if(e>=ti):
                e=0
                #print("Database Updated !!!!")
                c1.execute('''CREATE TABLE IF NOT EXISTS current(day integer PRIMARY KEY,a0 integer,a1 integer,a2 integer,a3 integer,a4 integer,a5 integer,a6 integer,a7 integer,a8 integer,a9 integer,a10 integer,a11 integer,a12 integer,a13 integer,a14 integer,a15 integer,a16 integer,a17 integer,a18 integer,a19 integer);''')
                conn1.commit()
                c1.execute("SELECT * FROM current")
                rows=c1.fetchall()
                #print(t[2])
                if(len(rows)== 0):
                        rows=[[0]]
                if(len(rows)!=0 and t[2] == str(rows[len(rows)-1][0])):
                        #print(0)
                        c1.execute("DELETE FROM current WHERE day ="+str(t[2]))
                        c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(t[2],rows[len(rows)-1][1]+self.tvar_data[0],rows[len(rows)-1][2]+self.tvar_data[1],rows[len(rows)-1][3]+self.tvar_data[2],rows[len(rows)-1][4]+self.tvar_data[3],rows[len(rows)-1][5]+self.tvar_data[4],rows[len(rows)-1][6]+self.tvar_data[5],rows[len(rows)-1][7]+self.tvar_data[6],rows[len(rows)-1][8]+self.tvar_data[7],rows[len(rows)-1][9]+self.tvar_data[8],rows[len(rows)-1][10]+self.tvar_data[9],rows[len(rows)-1][11]+self.tvar_data[10],rows[len(rows)-1][12]+self.tvar_data[11],rows[len(rows)-1][13]+self.tvar_data[12],rows[len(rows)-1][14]+self.tvar_data[13],rows[len(rows)-1][15]+self.tvar_data[14],rows[len(rows)-1][16]+self.tvar_data[15],rows[len(rows)-1][17]+self.tvar_data[16],rows[len(rows)-1][18]+self.tvar_data[17],rows[len(rows)-1][19]+self.tvar_data[18],rows[len(rows)-1][20]+self.tvar_data[19]))
                else:
                        #print(1)
                        for i in range(1,int(t[2])-rows[len(rows)-1][0]):
                                c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(rows[len(rows)-1][0]+i,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))                 
                        c1.execute("INSERT INTO current VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(t[2],self.tvar_data[0],self.tvar_data[1],self.tvar_data[2],self.tvar_data[3],self.tvar_data[4],self.tvar_data[5],self.tvar_data[6],self.tvar_data[7],self.tvar_data[8],self.tvar_data[9],self.tvar_data[10],self.tvar_data[11],self.tvar_data[12],self.tvar_data[13],self.tvar_data[14],self.tvar_data[15],self.tvar_data[16],self.tvar_data[17],self.tvar_data[18],self.tvar_data[19]))

                conn1.commit()
                self.tvar_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        #print(self.tvar_data)
        self.after(1000,self.showtime)

    def speech_rec(self):
            global nav
            w={"boys hostel 3" :39,"cs block" : 45,"it block" : 45,"computer science department" : 45,"civil department" : 45,"information technology department " : 45,"parking" :46,"sharan garg" :54,"indo german hospital" :54,"hospital" :54,"skill centre" :28,"mca block" :1,"tifac Core":1,"mba block":42,"workshop":96,"professor's parking":5,"main gate": 0,"girls hostel" :13,'temple' :73,'faith centre':73,'girls hostel 1' :65,'girls hostel 2' :67,'girls hostel 3' :62,'cs canteen' :79,'cafeteria':79,'boys hostel 2' :57,'near boys hostel':75,'senior boys hostel' :75,'mechanical canteen' :83,'me canteen' : 83,'mechanical block' :82,'lecture theatre' :93,'academic block' :91,'central library' : 91,'library' : 91,'electronics depertment' :89,'ece department' :89,'back block' : 89}
            '''
            r= sr.Recognizer()

            mic = sr.Microphone()


            with mic as source:
                    #r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)

            response = r.recognize_google(audio)

            print(response,w[response.lower()])
            '''
            if(nav == ''):
                    self.navi_box = AutocompleteEntry(w.keys(), self)
                    self.navi_box.grid(row=15, column=2,columnspan=3)
            else:
                    self.navi_box.destroy()
                    self.shortestPath(self.ax,self.canves,w[nav])
                    nav=''
             
    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        self.control=controller
        def key(event):
            self.pos.remove()
            c= str(repr(event.char))
            if c[1] == 'w':
                self.y=self.y+0.000028
            elif c[1] == 's':
                self.y=self.y-0.000028
            elif c[1] == 'a':
                self.x=self.x-0.000028
            elif c[1] == 'd':
                self.x=self.x+0.000028
            self.pos = self.ax.scatter(self.x,self.y)
            p=Point(self.x,self.y)
            for i in range(0,len(self.figures)):
                if self.figures[i].contains(p):
                    self.ax.set_title("Inside " + self.info[i+1])
                    self.cur=i+1
                    break
            else:
                self.cur=0
                self.ax.set_title("Inside AKGEC")
            self.canves.draw()
        def callback(event):
            frame.focus_set()
            print("Ready to go for the Virtual Tour ....")
            
        frame= Frame(self,width=100,height=100)
        frame.bind("<Key>", key)
        frame.bind("<Button-1>", callback)
        frame.grid(row=8,column=6)
        self.read_building_data()
        self.plot()
        
        self.canves = FigureCanvasTkAgg(self.fig, self)
        self.canves.get_tk_widget().grid(row=0,column=0,columnspan=4,rowspan=20,sticky='ew')
        self.canves.draw()
        self.base_map()
        self.boundaries()
        self.pos = self.ax.scatter(self.x,self.y)
        seconds = time.time()
        t = time.ctime(seconds)
        self.v = StringVar()
        Label(self, textvariable=self.v,height=1,width=20).grid(row=0,column=0,rowspan=2,columnspan=5)
        self.v.set(t)
        self.after(1000,self.showtime)
        


        b1= Button(self,text="Base Map",relief=FLAT, command = self.base_map)
        b1['font']=BFONT
        b1.grid(row=0,column=6, padx = 10)
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=1,column=6,sticky='ew')
        b2= Button(self,text="Boundaries",relief=FLAT, command = self.boundaries)
        b2['font']=BFONT
        b2.grid(row=2,column=6, padx = 10)
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=3,column=6,sticky='ew')
        b3= Button(self,text="scatter",relief=FLAT, command = self.scatter)
        b3['font']=BFONT
        b3.grid(row=4,column=6, padx = 10)
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=5,column=6,sticky='ew')
        b4= Button(self,text="Path",relief=FLAT,  command = self.path_draw)
        b4['font']=BFONT
        b4.grid(row=6,column=6, padx = 10)
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=7,column=6,sticky='ew')
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=12,column=6,sticky='ew')
        
        b5 = Button(self, text ="Profile",relief=FLAT, 
        command = lambda : controller.show_frame(Profile)) 

        b5['font']=BFONT
        b5.grid(row = 13, column = 6, padx = 10)
        sep = ttk.Separator(self, orient="horizontal")
        sep.grid(row=14,column=6,sticky='ew')
        b6 = Button(self, text ="Settings",relief=FLAT, 
        command = lambda : controller.show_frame(Settings))
        b6['font']=BFONT
        b6.grid(row = 15, column = 6, padx = 10)
        b7 = Button(self, text ="Analysis",relief=FLAT, 
        command = lambda : self.control.show_frame(Visualize))
        b7['font']=BFONT
        b7.grid(row = 10, column = 6, padx = 10)
        photo = PhotoImage(file = r"nav.png")
        self.photo = photo.subsample(3, 3)
        self.b8 = Button(self,image=self.photo,command=self.speech_rec)
        self.b8.image=photo
        self.b8.grid(row=15,column=3)
        sep1 = ttk.Separator(self, orient=VERTICAL)
        sep1.grid(row=0,column=4,sticky='ns',columnspan=2,rowspan=17)
        sep2 = ttk.Separator(self, orient=VERTICAL)
        sep2.grid(row=0,column=7,sticky='ns',columnspan=2,rowspan=17)
        sep3 = ttk.Separator(self, orient=HORIZONTAL)
        sep3.grid(row=9,column=6,sticky='ew')
        sep4 = ttk.Separator(self, orient=HORIZONTAL)
        sep4.grid(row=16,column=6,sticky='ew')


class Profile(tk.Frame):

  R=list()
  e=0

  def update(self):
        if self.t6.get().isdigit() and self.t6.get().isdigit() :
                print("Beautiful")
        else:
                messagebox.showinfo("Alert !!!!","Roll number and Student number should be number")
                return
        global c
        c.execute("UPDATE profile SET fname=?,mname=?,lname=?,branch=?,section=?,snumber=?,rnumber=?,gender=?,email=? WHERE id =1",(self.t1.get(),self.t2.get(),self.t3.get(),self.t4.get(),self.t5.get(),self.t6.get(),self.t7.get(),self.gender.get(),self.t9.get()))
        conn.commit()
        self.t1['state']=DISABLED
        self.t2['state']=DISABLED
        self.t3['state']=DISABLED
        self.t4['state']=DISABLED
        self.t5['state']=DISABLED
        self.t6['state']=DISABLED
        self.t7['state']=DISABLED
        self.R[0]['state']=DISABLED
        self.R[1]['state']=DISABLED
        self.t9['state']=DISABLED
  def feed(self): 
        
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.t4.delete(0,END)
        self.t5.delete(0,END)
        self.t6.delete(0,END)
        self.t7.delete(0,END)
        self.t9.delete(0,END)
        
        self.t1.insert(0,r1[0][1])
        self.t2.insert(0,r1[0][2])
        self.t3.insert(0,r1[0][3])
        self.t4.insert(0,r1[0][4])
        self.t5.insert(0,r1[0][5])
        self.t6.insert(0,r1[0][6])
        self.t7.insert(0,r1[0][7])
        self.R[int(r1[0][8])-1].invoke()
        self.t9.insert(0,r1[0][9])

        self.t1['state']=DISABLED
        self.t2['state']=DISABLED
        self.t3['state']=DISABLED
        self.t4['state']=DISABLED
        self.t5['state']=DISABLED
        self.t6['state']=DISABLED
        self.t7['state']=DISABLED
        self.R[0]['state']=DISABLED
        self.R[1]['state']=DISABLED
        self.t9['state']=DISABLED
        
        #print(rows)
        
  def edit(self):
          global r1
          if(r1[0][1] == ''):
                  messagebox.showinfo("Welcome !!!!"," Don't be shy to create your first profile (:- ")
          if self.e == 1:
                  self.e=0
                  self.t1['state']=DISABLED
                  self.t2['state']=DISABLED
                  self.t3['state']=DISABLED
                  self.t4['state']=DISABLED
                  self.t5['state']=DISABLED
                  self.t6['state']=DISABLED
                  self.t7['state']=DISABLED
                  self.R[0]['state']=DISABLED
                  self.R[1]['state']=DISABLED
                  self.t9['state']=DISABLED
                  
          else:
                  self.e=1
                  self.t1['state']=NORMAL
                  self.t2['state']=NORMAL
                  self.t3['state']=NORMAL
                  self.t4['state']=NORMAL
                  self.t5['state']=NORMAL
                  self.t6['state']=NORMAL
                  self.t7['state']=NORMAL
                  self.R[0]['state']=NORMAL
                  self.R[1]['state']=NORMAL
                  self.t9['state']=NORMAL
          
  def __init__(self, parent, controller):

    global r1
    
    tk.Frame.__init__(self, parent) 
    label = ttk.Label(self, text ="Profile", font = LARGEFONT) 
    label.grid(row = 0, column = 0,columnspan=5)
    f=LabelFrame(self,height=500,width=700,text="Information")
    f.grid(row = 3, column = 4,padx=10,rowspan=100,columnspan=100)
    l1=Label(self,text ="Name :", font = TFONT)
    l1.grid(row = 4, column = 5,padx=10,pady=10)
    l2=Label(self,text ="Branch :", font = TFONT)
    l2.grid(row = 5, column = 5,padx=10,pady=10)
    l3=Label(self,text ="Section :", font = TFONT)
    l3.grid(row = 6, column = 5,padx=10,pady=10)
    l4=Label(self,text ="Student Number :", font = TFONT)
    l4.grid(row = 7, column = 5,padx=10,pady=10)
    l5=Label(self,text ="Roll Number :", font = TFONT)
    l5.grid(row = 8, column = 5,padx=10,pady=10)
    l6=Label(self,text ="Gender :", font = TFONT)
    l6.grid(row = 9, column = 5,padx=10,pady=10)
    l7=Label(self,text ="Email Id :", font = TFONT)
    l7.grid(row = 10, column = 5,padx=10,pady=10)
    
    self.t1= Entry(self,width=15)
    self.t1.grid(row = 4, column = 7)
    self.t2= Entry(self,width=15)
    self.t2.grid(row = 4, column = 8)
    self.t3= Entry(self,width=15)
    self.t3.grid(row = 4, column = 9)
    self.t4= Entry(self,width=15)
    self.t4.grid(row = 5, column = 7)
    self.t5= Entry(self,width=15)
    self.t5.grid(row = 6, column = 7)
    self.t6= Entry(self,width=15)
    self.t6.grid(row = 7, column = 7)
    self.t7= Entry(self,width=15)
    self.t7.grid(row = 8, column = 7)
    self.gender = IntVar()
    self.R.append(Radiobutton(self, text="Male", variable=self.gender, value=1))
    self.R[0].grid(row = 9, column = 7)
    self.R.append(Radiobutton(self, text="Female", variable=self.gender, value=2))
    self.R[1].grid(row = 9, column = 8)
    self.t9= Entry(self,width=30)
    self.t9.grid(row = 10, column = 7,columnspan=2)
    
    self.feed()

    be = Button(self, text ="Edit",relief=GROOVE,command=self.edit)
    be['font']=BFONT
    be.grid(row = 12, column = 14,padx=10,pady=10)    
    b0 = Button(self, text ="Save",relief=GROOVE,command=self.update)
    b0['font']=BFONT
    b0.grid(row = 12, column = 15,padx=10,pady=10)
    

    b1 = Button(self, text ="Map",relief=FLAT, 
              command = lambda : controller.show_frame(StartPage))
    b1['font']=BFONT
    b1.grid(row = 2, column = 0,columnspan=2,padx=15,pady=10) 
    b2 = Button(self, text ="Settings",relief=FLAT, 
              command = lambda : controller.show_frame(Settings))
    b1['font']=BFONT
    b2.grid(row = 3, column = 0,columnspan=2,padx=15,pady=10)
    sep = ttk.Separator(self, orient=HORIZONTAL)
    sep.grid(row=1,column=0,sticky='ew',columnspan=25)
    sep = ttk.Separator(self, orient=VERTICAL)
    sep.grid(row=2,column=3,sticky='ns',rowspan=17,pady=5)

class Settings(tk.Frame):
  e=0
  def edit(self):
          if self.e == 1:
                  self.e=0
                  self.s['state']=DISABLED
                  self.popupMenu['state']=DISABLED
                  self.popupMenu1['state']=DISABLED
                  self.popupMenu2['state']=DISABLED
                  self.popupMenu3['state']=DISABLED
                  
          else:
                  self.e=1
                  self.s['state']=NORMAL
                  self.popupMenu['state']=NORMAL
                  self.popupMenu1['state']=NORMAL
                  self.popupMenu2['state']=NORMAL
                  self.popupMenu3['state']=NORMAL
  def feed(self):
        global r
        self.s.delete(0,END)
        self.s.insert(0,r[0][1])
        self.unit.set(r[0][2])
        self.b_color.set(r[0][3])
        self.e_color.set(r[0][4])
        self.l_color.set(r[0][5])
        self.s['state']=DISABLED
        self.popupMenu['state']=DISABLED
        self.popupMenu1['state']=DISABLED
        self.popupMenu2['state']=DISABLED
        self.popupMenu3['state']=DISABLED
        
  def save(self):
        global ti
        global units
        global b_color
        global e_color
        global l_color
        global c
        global conn
        #c.execute("DROP TABLE settings")
        c.execute("UPDATE settings SET refresh=?,unit=?,b_color=?,e_color=?,l_color=? WHERE id =1",(self.s.get(),self.unit.get(),self.b_color.get(),self.e_color.get(),self.l_color.get()))
        conn.commit()
        ti=int(self.s.get())
        units=self.unit.get()
        e_color=self.e_color.get()
        l_color=self.l_color.get()

        if self.b_color.get() == 'Random (try it)':
                b_color=[random.choice(['red','blue','green','pink','yellow','brown','cyan']) for i in range(0,17)]
        else:
                b_color=[self.b_color.get() for i in range(0,17)]

        self.s['state']=DISABLED
        self.popupMenu['state']=DISABLED
        self.popupMenu1['state']=DISABLED
        self.popupMenu2['state']=DISABLED
        self.popupMenu3['state']=DISABLED
        

        
  def __init__(self, parent, controller): 
    tk.Frame.__init__(self, parent)
    label = ttk.Label(self, text ="Settings", font = LARGEFONT, borderwidth=5) 
    label.grid(row = 0, column = 0, padx = 10, pady = 10,columnspan=10) 

    button1 = Button(self, text ="Map", relief=FLAT,
              command = lambda : controller.show_frame(StartPage)) 
    button1.grid(row = 2, column = 0, padx = 10, pady = 10)
    button2 = Button(self, text ="Profile",relief=FLAT,
              command = lambda : controller.show_frame(Profile)) 
    button2.grid(row = 3, column = 0, padx = 10, pady = 10)
    sep = ttk.Separator(self, orient=HORIZONTAL)
    sep.grid(row=1,column=0,sticky='ew',columnspan=40)
    sep = ttk.Separator(self, orient=VERTICAL)
    sep.grid(row=1,column=2,sticky='ns',rowspan=17,padx=10,pady=10)
    f=LabelFrame(self,height=500,width=820,text="Tool Box")
    f.grid(row = 3, column = 3,padx=10,rowspan=100,columnspan=100)

    l1 = Label(self, text ="Refresh Rate :", font = TFONT, borderwidth=5) 
    l1.grid(row = 3, column = 4, padx = 10, pady = 20)
    l2 = Label(self, text ="Unit of Time :", font = TFONT, borderwidth=5) 
    l2.grid(row = 4, column = 4, padx = 10)
    l3 = Label(self, text ="Secs", font = BFONT, borderwidth=5) 
    l3.grid(row = 3, column = 6, pady = 20)
    l4 = Label(self, text ="Bars Colour :", font = TFONT, borderwidth=5) 
    l4.grid(row = 5, column = 4, pady = 20)
    l5 = Label(self, text ="Edge Colour :", font = TFONT, borderwidth=5) 
    l5.grid(row = 6, column = 4, pady = 20)
    l6 = Label(self, text ="Labels Colour :", font = TFONT, borderwidth=5) 
    l6.grid(row = 7, column = 4, pady = 20)
    self.s = Spinbox(self, from_=0, to=30,width=5)
    self.s.grid(row = 3, column = 5, padx = 10, pady = 20)
    b1=Button(self, text ="Edit", relief=GROOVE,
              command = self.edit) 
    b1.grid(row = 90, column = 82, padx = 10)
    b1=Button(self, text ="Save", relief=GROOVE,
              command = self.save) 
    b1.grid(row = 90, column = 84, padx = 10)
    choices={'Sec','Min','Hour'}
    choices1={'red','blue','green','pink','yellow','brown','cyan','Random (try it)'}
    choices2={'black','red','blue','green','pink','yellow','brown','cyan'}
    choices3={'black','red','blue','green','pink','yellow','brown','cyan'}
    self.unit = StringVar(self)
    self.b_color = StringVar(self)
    self.e_color = StringVar(self)
    self.l_color = StringVar(self)
    self.popupMenu = OptionMenu(self, self.unit, *choices)
    self.popupMenu.grid(row = 4, column =5)
    self.popupMenu1 = OptionMenu(self, self.b_color, *choices1)
    self.popupMenu1.grid(row = 5, column =5)
    self.popupMenu2 = OptionMenu(self, self.e_color, *choices2)
    self.popupMenu2.grid(row = 6, column =5)
    self.popupMenu3 = OptionMenu(self, self.l_color, *choices3)
    self.popupMenu3.grid(row = 7, column =5)

    self.feed()

class Visualize(tk.Frame):
  fig=None
  p=[]
  

  d=['Free Roaming','CS/IT Block', 'Main Block', 'Back Block', 'Faith Centre', 'MCA Block', 'Mechanical Block', 'Skill Centre', 'Tiffac Core', 'Mechanical Canteen', 'Workshop', 'Professors Parking', 'Lecture Theaters', 'Girls Hostel 1', 'Girls Hostel 2', 'Parking','Girls Hostel 3','Senior Boys Hostel','Boys Hostel 2','Boys Hostel 3','All']
  def refresh(self):
          global conn1
          global c1
          global units
          global ti
          self.h_f=60
          c1.execute('''CREATE TABLE IF NOT EXISTS current
             (day integer PRIMARY KEY,a0 integer,a1 integer,a2 integer,a3 integer,a4 integer,a5 integer,a6 integer,a7 integer,a8 integer,a9 integer,a10 integer,a11 integer,a12 integer,a13 integer,a14 integer,a15 integer,a16 integer,a17 integer,a18 integer,a19 integer);''')
          c1.execute("SELECT * FROM current")
          self.rows=c1.fetchall()
          if(len(self.rows) == 0):
                  messagebox.showinfo("Welcome !!!!","It seems you visited here for the first time please wait for a while . we are preparing tasty cookies for you (:-")
                  self.after(1000,self.refresh)
                  ti=10
                  
          if(units == 'Min'):
                  self.h_f=2
                  self.rows=[[j+1]+[round(i/60,2) for i in self.rows[j][1:]] for j in range(0,len(self.rows))]
          elif(units == 'Hour'):
                  self.h_f=2
                  self.rows=[[j+1]+[round(i/3600,2) for i in self.rows[j][1:]] for j in range(0,len(self.rows))]
          #print(self.rows)
  def update_annot(self,bar):
    x = int(bar.get_x()+bar.get_width()/2.)
    y = bar.get_y()+bar.get_height()
    self.annot.xy = (x,y)
    text = "({})".format( self.d[x-1] )
    self.annot.set_text(text)
    self.annot.get_bbox_patch().set_alpha(0.4)


  def hover(self,event):
    vis = self.annot.get_visible()
    if event.inaxes == self.ax:
        for bar in self.bars:
            cont, ind = bar.contains(event)
            if cont:
                self.update_annot(bar)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
                self.canves.draw()
                return
    if vis:
        self.annot.set_visible(False)
        self.fig.canvas.draw_idle()
        self.canves.draw()
        
  def bar(self):

    global b_color
    global e_color
    global l_color
    global units

    if(self.fig != None):
            plt.close(self.fig)
            self.canves.get_tk_widget().destroy()
            try:
                    self.popupMenu.destroy()
                    self.popupMenu1.destroy()
                    self.l1.destroy()
            except:
                    print()
    
    self.fig, self.ax = plt.subplots(figsize = (7,4))
    self.ax.set_xlim(0,25)
    self.ax.set_ylim(0,max(self.rows[int(self.plot_date[1])-1][1:])+self.h_f)
    self.canves = FigureCanvasTkAgg(self.fig, self)
    self.canves.get_tk_widget().grid(row=4,column=4,columnspan=55,rowspan=20,padx=70,sticky='ew')
    plt.xticks([])
    plt.xlabel('Activity', fontsize=18)
    plt.ylabel('Time ( ' + units + ')', fontsize=16)
    self.bars = self.ax.bar([i for i in range(1,len(self.rows[0]))],self.rows[int(self.plot_date[1])-1][1:],edgecolor=e_color,color=b_color)
    self.annot = self.ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",bbox=dict(boxstyle="round", fc=l_color, ec="r", lw=2),arrowprops=dict(arrowstyle="->"))
    self.annot.set_visible(False)
    self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
    self.canves.draw()
  def select_date(self):
          root = Tk()

          root.title("Select Date")
          ws = self.winfo_screenwidth()
          hs = self.winfo_screenheight()
          x = (ws/4)
          y = (hs/4)
          root.geometry('+%d+%d' % (x, y))

          c= Calendar(root,selectmode="day",year=2020,month=7,day=self.rows[len(self.rows)-1][0])

          c.grid(row=2,column=5)

          def grab():
                  self.plot_date=str(c.get_date()).split("/")
                  self.l['text']=str(c.get_date())
                  root.destroy()

          b=Button(root,text="Select",command=grab)
          b.grid(row=3,column=5,padx=5)

          root.mainloop()

  def ann(self,a):
          if(a == 'All'):
                  self.p=list(range(0,20))
          else:
                  self.p=[self.d.index(self.f.get()),self.d.index(self.s.get())]
          self.l_charts()
  def l_charts(self):
          if(self.fig != None):
            plt.close(self.fig)
            self.canves.get_tk_widget().destroy()
            try:
                    self.popupMenu.destroy()
                    self.popupMenu1.destroy()
                    self.l1.destroy()
            except:
                    print()
            
          self.popupMenu = OptionMenu(self, self.f, *self.d, command= self.ann)
          self.popupMenu.grid(row = 90, column =50)
          self.popupMenu1 = OptionMenu(self, self.s, *self.d, command= self.ann)
          self.popupMenu1.grid(row = 90, column =52)
          self.l1 = Label(self, text ="Vs", font = BFONT, borderwidth=5) 
          self.l1.grid(row = 90, column = 51, pady = 20)
          self.fig, self.ax = plt.subplots(figsize = (7,4))
          plt.xlabel('Day', fontsize=12)
          plt.ylabel('Time ( ' + units + ')', fontsize=12)
          self.canves = FigureCanvasTkAgg(self.fig, self)
          self.canves.get_tk_widget().grid(row=4,column=4,columnspan=55,rowspan=20,padx=70,sticky='ew')
          
          for k in self.p:
                  self.ax.plot([i for i in range(1,len(self.rows)+1)],[i[k+1] for i in self.rows],label=f"${self.d[k]}$")
                  
          mplcursors.cursor(self.fig,hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
          

  
          
  def __init__(self, parent, controller): 
    tk.Frame.__init__(self, parent)
    global ti
    label = ttk.Label(self, text ="Analysis", font = LARGEFONT) 
    label.grid(row = 0, column = 0,columnspan=5,padx=10)
    b1 = Button(self, text ="Map",relief=FLAT,command = lambda : controller.show_frame(StartPage))
    b1['font']=BFONT
    b1.grid(row = 2, column = 0,columnspan=2,padx=15,pady=10) 
    b2 = Button(self, text ="Profile",relief=FLAT, 
              command = lambda : controller.show_frame(Profile))
    b2['font']=BFONT
    b2.grid(row = 3, column = 0,columnspan=2,padx=15,pady=10)
    b3 = Button(self, text ="Settings",relief=FLAT, 
              command = lambda : controller.show_frame(Settings))
    b3['font']=BFONT
    b3.grid(row = 4, column = 0,columnspan=2,padx=15,pady=10)
    b4 = Button(self, text ="Plot",relief=GROOVE, 
              command = self.bar)
    b4['font']=BFONT
    b4.grid(row = 2, column = 6,pady=10,padx=10)
    b5 = Button(self, text ="Choose",relief=GROOVE, 
              command = self.select_date)
    b5['font']=BFONT
    b5.grid(row = 2, column = 5,pady=10)
    b6 = Button(self, text ="Refresh",relief=GROOVE, 
              command = self.refresh)
    b6['font']=BFONT
    b6.grid(row = 1, column = 45,pady=10,padx=10)
    b7 = Button(self, text ="Growth",relief=GROOVE, 
              command = self.l_charts)
    b7['font']=BFONT
    b7.grid(row = 2, column = 7,pady=10,padx=10)
    self.l= Label(self,text="Choose....",font=BFONT)
    self.l.grid(row = 2, column = 4)
    sep = ttk.Separator(self, orient=HORIZONTAL)
    sep.grid(row=1,column=0,sticky='ew',columnspan=40)
    sep = ttk.Separator(self, orient=VERTICAL)
    sep.grid(row=2,column=2,sticky='ns',rowspan=17,pady=5)
    f=LabelFrame(self,height=500,width=820,text="Playground")
    f.grid(row = 3, column = 4,padx=10,rowspan=100,columnspan=100)
    self.f = StringVar(self)
    self.s = StringVar(self)
    self.f.set('CS/IT Block')
    self.s.set('Main Block')
    self.p=[self.d.index(self.f.get()),self.d.index(self.s.get())]
    self.refresh()
    
    

app = SMSApp()
app.mainloop()

