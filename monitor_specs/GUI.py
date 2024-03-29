#!/usr/bin/env python3

from tkinter import *
import tkinter as tk
from GUI_helper import *
import math

monitor=[]
monitorData={}
queue=[]
ignore_list=[];

#------------------------------------------------

def refresh(event=None):
    data=refresh_information(ignore_list)
    num=0
    
    if(num>len(data)-1):
        print("ERROR: Selected Monitor Not Found")
        return

    monitor[0][1].delete(0, tk.END)
    monitor[0][1].insert(0, data[num]["vendor"].title())

    x=int(data[num]["size"][0])
    y=int(data[num]["size"][1])
    monitor[1][1].delete(0, tk.END)
    monitor[1][1].insert(0, round(2*math.sqrt(x*x+y*y)*0.0393701)/2)

    monitor[2][1].delete(0, tk.END)
    monitor[2][1].insert(0, data[num]["resolution"])

    monitor[3][1].select()
    monitor[4][1].select()
    monitor[5][1].deselect()
    monitor[6][1].deselect()

    monitor[7][1].delete(0, tk.END)


def add(event=None):
    data={}
    data["vendor"]=monitorData["vendor_val"].get()
    data["resolution"]=monitorData["resolution_val"].get()
    data["size"]=monitorData["size_val"].get()
    data["interfaces"]=monitorData["VGA_VAL"].get()+monitorData["DVI_VAL"].get()+monitorData["DP_VAL"].get()+monitorData["HDMI_VAL"].get()+" "+monitorData["OTHER_VAL"].get()
    queue.append(data)
    print("Q: "+str(len(queue))+"; Added: "+data["vendor"]+" - "+data["size"])


def remove(event=None):
    data = queue.pop()
    print("Q: "+str(len(queue))+"; Removed: "+data["vendor"]+" - "+data["size"])

def print_file(event=None):
    global queue
    global old_queue
    if(len(queue)!=0):
        old_queue = queue.copy()
        flushQueue(queue)
    queue=[]

def reprint_file(event=None):
    global old_queue
    if(len(old_queue)!=0):
        flushQueue(old_queue)

#------------------------------------------------


def generateGrid(grid, stick): 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j]!=None):
                grid[i][j].grid(row=i, column=j, sticky=stick[j])


def generateMonitorGrid(base):
    grid=[]
    sticky=["NE", "NW"]
    
    grid.append([Label(base, text="Vendor:"), Entry(base, textvariable=monitorData["vendor_val"])])
    
    grid.append([Label(base, text="Size:"), Entry(base, textvariable=monitorData["size_val"])])
    
    grid.append([Label(base, text="Resolution:"), Entry(base, textvariable=monitorData["resolution_val"])])
    

    grid.append([Label(base, text="Interfaces:"), Checkbutton(base, 
        text="VGA", 
        variable=monitorData["VGA_VAL"], 
        onvalue=" VGA", 
        offvalue="")])
    grid.append([None, Checkbutton(base, 
        text="DVI", 
        variable=monitorData["DVI_VAL"], 
        onvalue=" DVI", 
        offvalue="")])
    grid.append([None, Checkbutton(base, 
        text="DP", 
        variable=monitorData["DP_VAL"],
        onvalue=" DP", 
        offvalue="")])
    grid.append([None, Checkbutton(base, 
        text="HDMI", 
        variable=monitorData["HDMI_VAL"], 
        onvalue=" HDMI", 
        offvalue="")])
    grid.append([None, Entry(base, textvariable=monitorData["OTHER_VAL"])])
    
    generateGrid(grid, sticky)
    return grid

 
def generateButtonsGrid(base):
    grid=[]

    grid.append([Button(base, text="Add", command=add)])
    grid.append([Button(base, text="Refresh", command=refresh)]) 
    grid.append([Button(base, text="Print", command=print_file)])
    grid.append([Button(base, text="(Remove)", command=remove)])
    grid.append([Button(base, text="(Reprint)", command=reprint_file)])

    generateGrid(grid, ["NSEW"])
    return grid


with open(os.path.expanduser("~/.config/ReUseAutomation/monitor_specs/ignore.txt")) as ignore_file:
    for line in ignore_file:
        ignore_list.append(line.strip())

root=Tk()
monitorData={
        "VGA_VAL" : StringVar(),
        "DVI_VAL" : StringVar(),
        "DP_VAL" : StringVar(),
        "HDMI_VAL" : StringVar(),
        "OTHER_VAL" : StringVar(),
        "vendor_val" : StringVar(),
        "size_val" : StringVar(),
        "resolution_val" : StringVar()}
root.title("Monitor Information")
root.bind("<Control-r>", refresh)
root.bind("<Control-a>", add)
root.bind("<Control-p>", print_file)
fr_entry=Frame(master=root, width=150)
fr_buttons=Frame(master=root, width=50)
fr_entry.grid(row=0, column=0)
fr_buttons.grid(row=0, column=1)

monitor=generateMonitorGrid(fr_entry)

generateButtonsGrid(fr_buttons)

root.mainloop()
