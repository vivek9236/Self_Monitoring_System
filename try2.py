from tkinter import * 
  

root = Tk() 

photo = PhotoImage(file = r"mic.png") 
  
Button(root, image = photo).grid(row=0,column=0) 
  
mainloop() 
