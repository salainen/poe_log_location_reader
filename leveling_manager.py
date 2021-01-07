import tkinter
from tkinter import *
from tkinter import filedialog
import os
import time
import threading

# set location for the leveling_setup.txt:
dir_path = os.path.dirname(os.path.realpath(__file__))
leveling_text = dir_path + "/leveling_setup.txt"

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
                level_data.pop(x)
                break

def follow(client_log):
    
    ''' check target file for changes

    '''
    # end of file
    client_log.seek(0,2) 
    while True:
        line = client_log.readline()
        if not line:
            # we want a small sleep here
            # no need to burn CPU
            time.sleep(1) 
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

def init_window():

    ''' handles main ui creation

    '''

    # Add delete row button
    delete_button = tkinter.Button(root , text = 'Delete selected Row', command = delete_row)
    delete_button.grid(row =0, column=0)

    # Add header row
    select_text = StringVar()
    entry_1 = Entry(root, textvariable = select_text, state = 'readonly')
    select_text.set('Select')
    entry_1.grid(row = 1, column = 0 )

    info_labels = StringVar()
    entry_2 = Entry(root, textvariable = info_labels, state = 'readonly', width=20)
    info_labels.set('Place')
    entry_2.grid(row = 1, column = 1 )

    info_labels = StringVar()
    entry_2 = Entry(root, textvariable = info_labels, state = 'readonly', width=100)
    info_labels.set('Notes')
    entry_2.grid(row = 1, column = 2 )

# main stuff under this line:

# open leveling notes:
with open(leveling_text) as f:
    level_data = f.readlines()

level_data = [x.strip() for x in level_data]

# create the main window:
i=2
rows = []
root = Tk()

init_window()

# open file dialog:
log_file_name = None
while not log_file_name:
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Open Client.txt",filetypes = (("client log","*.txt"),("all files","*.*")))
    print (root.filename)
    log_file_name = root.filename
root.title("Monitoring: " + log_file_name)

# start file monitoring thread:
file_reader = threading.Thread(target=task_master, args=(1,))
file_reader.start()

# make sure our window stays on top:
root.wm_attributes("-topmost", 1)

# start main tkinter loop:
mainloop()