import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
#hello
x,y=77.5031,28.67535
da=pd.read_csv('route.txt')
a=list(da.longitude)
b=list(da.latitude)
points=[]
for i in range(len(a)):
    points.append([a[i]-x,b[i]-y])
    
K=1
points.sort(key = lambda K: K[0]**2 + K[1]**2)
print(list(da[da.longitude == (points[:K][0][0]+x)].sno)[0])
