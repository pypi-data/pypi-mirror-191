import ast
import threading
import pyautogui as pg
from PIL import Image
import os
import time
import tkinter as tk
import sys

def countdown():
    global seconds
    global startbutton
    global tkWindow
    real_sec = seconds
    seconds = seconds + 4
    tkWindow = tk.Tk()
    tkWindow.geometry('295x367')
    tkWindow.title('KeyloggerScreenshot')
    minutes = seconds // 60
    this_min = minutes * 60
    this_sec = seconds - this_min
    print(f"This simulation will last for {minutes} minutes and {this_sec} seconds")

    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"\rTime left: {timer}", end="")
        time.sleep(1)
        seconds -= 1

    startbutton = tk.Button(tkWindow, text="Stop stimulation", command=changecol, height=10, width=30)
    startbutton.grid(row=1, column=0)
    if real_sec < 60: text =f"Simulation for {real_sec} seconds"
    else:
        m, s = divmod(real_sec, 60)
        timer = '{:02d}:{:02d}'.format(m, s)
        text = f"Simulation for {timer} minutes"
    tk.Button(tkWindow, text=text, command=connection, height=10, width=30).grid(row=2, column=0)
    tkWindow.mainloop()

def changecol():
    startbutton.configure(bg="red")
    startbutton["text"] = "Stop simulation"
    tkWindow.destroy()

def connection(): print("Successful connection")

if "fullscreen.png" not in os.listdir():
    print('"fullscreen.png" is not in your directory. Download the image on '
          'https://github.com/Kill0geR/KeyloggerScreenshot')
    sys.exit()

if sys.platform != "linux":
    print("This simulation is only availible on linux. The Windows version is coming soon")
    sys.exit()

mouse_coordinates = [mouse for mouse in os.listdir() if "mouseInfoLog" in mouse]

if not mouse_coordinates:
    print("The target hasn't clicked anything")
    sys.exit()

every_coordinate = []
for each_core in mouse_coordinates:
    fhandle = open(each_core)
    for line in fhandle:
        if "[" in line:
            every_coordinate += ast.literal_eval(line)

img_files = [each_img for each_img in os.listdir() if "New_Image" in each_img]
if not img_files:
    print('There is no "New_Image" in this directory')
    sys.exit()

speed = 0.46
sleep = 1.5
one_coordinate = speed + sleep

duration_seconds = one_coordinate * len(every_coordinate)
summed_up = duration_seconds * len(img_files) + 2 * len(img_files)
seconds = round(summed_up)

print(f"The target has clicked {len(every_coordinate)} times on his screen")
threading_count = threading.Thread(target=countdown)
threading_count.start()
pg.sleep(4)
for image in img_files:
    im = Image.open(image)
    im.show()
    time.sleep(2)
    fullscreen = pg.locateCenterOnScreen("fullscreen.png")
    if fullscreen:
        pg.click(fullscreen)
        for x, y in every_coordinate:
            pg.moveTo(x, y, 0.3)
            time.sleep(sleep)
        pg.press("esc")