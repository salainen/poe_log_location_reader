from tkinter import *
import tkinter
import os
import time
import sys
import threading

dir_path = os.path.dirname(os.path.realpath(__file__))
leveling_text = dir_path + "/leveling_setup.txt"
log_file_name = dir_path + "/Client.txt"

global level_data

def read_instructions(line):

    ''' finds instructions based on location

    Reads location data from log file line, then checks
    it against leveling data, if match is found, it'll
    call add_row() function to add a new row in the GUI
    with the location and instruction data.
    '''

    global level_data
    
    # extracting the location information:
    #2020/12/31 09:38:46 291455000 ba9 [INFO Client 457032] : You have entered Oriath.
    check_this_line = line

    # : You have entered Oriath.
    check_this_line = check_this_line.split(']')[1]
    
    #Oriath.
    check_this_line = check_this_line[20:]

    check_this_line = check_this_line.split('.')[0]

    # start looping the level data through to find the relevant notes:
    for x in range(0, len(level_data), 1):

        if "|" in level_data[x]:
            
            check_line = level_data[x].split('|')[1]
            if check_this_line.lower() in level_data[x].lower():

                add_row(level_data[x])

def follow(thefile):
    
    ''' check target file for changes

    '''
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(1) # Sleep briefly
            continue
        yield line

def task_master(name):

    ''' Monitoring thread 
    
    Monitors the Client.txt for area change, if found
    will call read_instructions() function

    '''
    logfile = open(log_file_name,"r")
    loglines = follow(logfile)
    for line in loglines:
        if " : You have entered " in line:
            read_instructions(line)



def add_row(text_to_add):

    ''' adds new row to the GUI

    expected input format:
    location|notes go here
    will create two column row with first column
    containing the location data, and second column
    containing the notes related to the location.
    '''

    location_data = text_to_add.split('|')[0]
    notes_data = text_to_add.split('|')[1]
    global i 
    i=i+1
    items = []
    var = IntVar()
    c = Checkbutton(root, variable = var)
    c.val = var
    items.append(c)
    c.grid(row = i, column = 0)
    b = Entry(root, width=20)
    b.insert(END, location_data)
    items.append(b)
    b.grid(row=i, column=1)

    d = Entry(root, width=100)
    d.insert(END, notes_data)
    items.append(d)
    d.grid(row=i, column=2)

    rows.append(items)

def delete_row():

    ''' deletes row(s) from the GUI

    '''

    for rowno, row in reversed(list(enumerate(rows))):
    
        if row[0].val.get() == 1:
    
            for i in row:
                i.destroy()
            rows.pop(rowno)

# main stuff under this line:
with open(leveling_text) as f:
    level_data = f.readlines()

level_data = [x.strip() for x in level_data]
#print(level_data)
i=2
rows = []
root = Tk()

# Add delete row button
dl = tkinter.Button(root , text = 'Delete selected Row', command = delete_row)
dl.grid(row =0, column=0)

v0 = StringVar()
e0 = Entry(root, textvariable = v0, state = 'readonly')
v0.set('Select')
e0.grid(row = 1, column = 0 )

# Add header row
v1 = StringVar()
e1 = Entry(root, textvariable = v1, state = 'readonly', width=20)
v1.set('Place')
e1.grid(row = 1, column = 1 )

v1 = StringVar()
e1 = Entry(root, textvariable = v1, state = 'readonly', width=100)
v1.set('Notes')
e1.grid(row = 1, column = 2 )

# start file monitoring thread:
file_reader = threading.Thread(target=task_master, args=(1,))
file_reader.start()

#root.wm_geometry("400x50")

# start main tkinter loop:
mainloop()