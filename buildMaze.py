""" GUI to build a maze and convert into prolog file.
    The Maze is a matrix of cells. Index starts from 1.
    The Write button generates a prolog file.
    Program can be invoked with no params or 1 or 2.
    No params generates a 10x10 matrix.
    One params n (int) generates a nxn matrix.
    Two params n,m (int) generates a nxm matrix.
    COLORS OF CELLS:
        - WHITE: empty
        - BLACK: occupied (wall)
        - GREEN: initial position (ONLY ONE)
        - RED: final position (exit) (MULTY)
"""
import sys
import tkinter as tk
from tkinter import W, Button, TOP, X, FLAT, LEFT, NW
#Gui height and width
width=500
height=500
# Set number of rows and columns
ROWS = 10
COLS = 10
# Struct for occupied cells
occupied = []
init_row = -1
init_col = -1
finals = []


# Event Listener. Get the square and change its color.
def callback(event):    
    # Calculate column and row number
    col = event.x//cellwidth
    row = event.y//cellheight
    item_id = rect[row,col]
    color = c.itemcget(item_id, "fill")
    # from occupied to finale
    if color=="black":
        c.itemconfig(item_id, fill="red")
        occupied.remove([row+1,col+1])
        finals.append([row+1,col+1])
    # from finale to initial
    elif color=="red":
        c.itemconfig(item_id, fill="green")
        finals.remove([row+1,col+1])
        global init_row
        global init_col
        if init_row > -1:
            ini_item_id = rect[init_row,init_col]
            c.itemconfig(ini_item_id, fill="white")
        init_row = row
        init_col = col
    # from initial to empty
    elif color=="green":
        init_row = -1
        init_col = -1
        c.itemconfig(item_id, fill="white")    
    # from empty to occupied
    else:
        c.itemconfig(item_id, fill="black")
        occupied.append([row+1,col+1])
#writing prolog file
def writePrologFile():
    f= open("maze.pl","w+")
    f.write("num_row({}).\n".format(ROWS))
    f.write("num_col({}).\n".format(COLS))
    occupied.sort()
    for _,pos in enumerate(occupied):
        f.write("occupied(pos({},{})).\n".format(pos[0],pos[1]))
    if(init_row>-1):
        f.write("initial(pos({},{})).\n".format(init_row+1,init_col+1))
    if len(finals):
        for _,fin in enumerate(finals):
            f.write("finale(pos({},{})).\n".format(fin[0],fin[1]))
# Set number of rows and columns

if len(sys.argv)==3:
    ROWS = int(sys.argv[1])
    COLS = int(sys.argv[2])
elif len(sys.argv)==2:
    ROWS = int(sys.argv[1])
    COLS = int(sys.argv[1])
else:
    ROWS = 10
    COLS = 10
# Create the window, to canvas and the mouse click event binding
root = tk.Tk()
c = tk.Canvas(root, width=500, height=500, borderwidth=5, background='black')
button1 = Button(text = "Write", command = writePrologFile,anchor = W)
button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
button1_window = c.create_window(10, 10, anchor=NW, window=button1)
button1.pack(side=tk.RIGHT, anchor=tk.SE)

c.pack(anchor=tk.NW, expand="true")
c.bind("<Button-1>", callback)
c.bind(button1, "<Button-1>", writePrologFile)
root.update()
#dimension of single square
cellwidth = c.winfo_width()//COLS
cellheight = c.winfo_height()//ROWS


rect = {}
for column in range(COLS):
            for row in range(ROWS):
                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                rect[row,column] = c.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
root.mainloop()