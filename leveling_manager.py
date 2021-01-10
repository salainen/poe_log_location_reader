import tkinter
from tkinter import *
from tkinter import filedialog


import os
import time
import threading
import datetime

# set location for the leveling_setup.txt:
dir_path = os.path.dirname(os.path.realpath(__file__))
leveling_text = dir_path + "/leveling_setup.txt"

global level_data
global stop_time
stop_time = False
global time_at_stop

time_at_stop = ""

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

    # split location_data | notes_data into two:
    location_data = text_to_add.split('|')[0]
    notes_data = text_to_add.split('|')[1]

    global i 
    i=i+1

    items = []
    var = IntVar()

    # print(i)
    to_be_deleted = i-2
    delete_entry = tkinter.Button(root , text = 'del', command = lambda: delete_row(to_be_deleted))
    delete_entry.grid(sticky="E,W", row=i, column=0)
    rows.append(delete_entry)

    # create notes label:
    notes_label = Entry(root)
    notes_label.insert(END, notes_data)
    items.append(notes_label)
    notes_label.grid(sticky="E,W", row=i, column=1, columnspan=2)

    # add all added items to rows -list:
    rows.append(items)
    row_index.append(i)


def delete_row(index_to_delete):

    ''' deletes a row from the GUI

    When del button is pressed, the del button
    and the text label in the same row will be
    deleted from the GUI.

    '''
    # calculate the button and text label positions
    # in the rows -list
    delete_this = index_to_delete*2-1
    delete_this2 = index_to_delete*2-2

    # delete the objects from GUI:
    for x in rows[delete_this]:
            x.destroy()
    rows[delete_this2].destroy()

def start_timer():

    ''' Starts the timer
    
    Starts the timer via starting a new thread timer_thread()
    Also sets the global flag stop_time to False
    '''
    
    global stop_time
    global time_at_stop
    stop_time = False
    timer = threading.Thread(target=timer_thread, args=(1,))
    timer.start()

def stop_timer():

    ''' Stops the timer

    '''

    for x in timer_store:
        x.destroy()

    # Stop start clock button
    timer_start_button = tkinter.Button(root , text = 'Start timer', command = start_timer)
    timer_start_button.grid(sticky="E,W", row=0, column=0)
    timer_store.append(timer_start_button)
    
    
    global stop_time
    stop_time = True

def timer_thread(time_arg):

    ''' Timer thread

    As long as global variable stop_time is set to False, 
    the timer will run. It'll update timer_text label 
    every 10 milliseconds.

    If timer has been previously started and then stopped
    the counter will resume from time_at_stop value.
    '''
    for x in timer_store:
        x.destroy()

    # Stop start clock button
    timer_stop_button = tkinter.Button(root , text = 'Stop timer', command = stop_timer)
    timer_stop_button.grid(sticky="E,W", row=0, column=0)
    timer_store.append(timer_stop_button)
        
    # creates the timer label in the main UI
    timer_text = StringVar()
    timer_label = Entry(root, textvariable = timer_text, state = 'readonly', width=12)
    timer_text.set('00:00:00')
    timer_label.config(font=("Courier", 30))
    
    timer_label.grid(sticky="E,W", row=0, column=1)

    global stop_time
    global time_at_stop

    # time when the thread was called:

    start_time = datetime.datetime.now()

    # if time_at_stop is set, use it
    if len(str(time_at_stop)) >= 1:
        start_time = datetime.datetime.now() - time_at_stop


    # thread loop. loop until stop_time global variable is set
    # to True:
    while not stop_time:
        time.sleep(0.01)
        current_time = datetime.datetime.now()

        # calculate time from thread start vs. current time.
        time_difference = current_time - start_time
        
        # set the label text:
        timer_text.set(str(time_difference)[:-3])
        time_at_stop = time_difference

def border_remove():

    ''' removes window borders

    '''
    for x in borders_store:
        x.destroy()
    root.overrideredirect(1)
    add_borders = tkinter.Button(root , text = 'add borders', command = border_add)
    add_borders.grid(sticky="E,W", row=0, column=2)
    borders_store.append(add_borders)

def border_add():

    ''' re-adds window borders

    '''
    for x in borders_store:
        x.destroy()
    root.overrideredirect(0)
    remove_borders = tkinter.Button(root , text = 'remove borders', command = border_remove)
    remove_borders.grid(sticky="E,W", row=0, column=2)
    borders_store.append(remove_borders)

def init_window():

    ''' handles main ui creation

    '''

    # Add start clock button
    timer_start_button = tkinter.Button(root , text = 'Start timer', command = start_timer)
    timer_start_button.grid(sticky="E,W", row=0, column=0)
    
    timer_store.append(timer_start_button)

    # add remove borders button
    remove_borders = tkinter.Button(root , text = 'remove borders', command = border_remove)
    remove_borders.grid(sticky="E,W", row=0, column=2)
    
    borders_store.append(remove_borders)

    timer_text = StringVar()
    timer_label = Entry(root, textvariable = timer_text, state = 'readonly', width=12)
    timer_text.set('0:00:00.000')
    timer_label.config(font=("Courier", 30))
    
    timer_label.grid(sticky="E,W", row=0, column=1)

# main stuff under this line:

# open leveling notes:
with open(leveling_text) as f:
    level_data = f.readlines()

level_data = [x.strip() for x in level_data]

# create the main window:
i=2
rows = []
row_index = []
root = Tk()


borders_store = []
timer_store = []

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
# root.overrideredirect(1)

# start main tkinter loop:
mainloop()