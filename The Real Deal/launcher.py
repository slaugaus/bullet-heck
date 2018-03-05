# Warning: Spaghetti code below.
# Actual necessary libs
import tkinter as tk
from tkinter import ttk
import pickle
import runpy
import sys
import os
from PIL import Image, ImageTk
# Libs used by the target file (needed for compilation)
import pygame
import random
# Define the windows.
main_win = tk.Tk()
main_win.title("Bullet Heck! Launcher")
main_win.resizable(False, False)
sett_win = tk.Toplevel()
sett_win.title("Settings")
sett_win.protocol("WM_DELETE_WINDOW", sett_win.withdraw)
sett_win.resizable(False, False)
# Create and/or load settings.pkl
try:
    file = open("settings.pkl", mode="r+b")
    vars = pickle.load(file)
    settings_exist = True
except FileNotFoundError:
    file = open("settings.pkl", mode="w+b")
    file = open("settings.pkl", mode="r+b")
    settings_exist = False
# Variables that will be written to settings
gamepad_connected = tk.BooleanVar(sett_win)
screen_width = tk.IntVar(sett_win)
screen_height = tk.IntVar(sett_win)
gamepad_id = tk.IntVar(sett_win)
deadzone = tk.DoubleVar(sett_win)
axis_x = tk.IntVar(sett_win)
axis_y = tk.IntVar(sett_win)
hat_id = tk.IntVar(sett_win)
show_fps = tk.BooleanVar(sett_win)
# Set the default values of the variables
if not settings_exist:
    gamepad_connected.set(False)
    screen_width.set(1600)
    screen_height.set(900)
    gamepad_id.set(0)
    deadzone.set(0.2)
    axis_x.set(0)
    axis_y.set(1)
    hat_id.set(0)
    show_fps.set(False)


def launch(file="BulletHeck.py"):
    """Run another .py."""
    if file == "BulletHeck.py":
        sett_win.destroy()
        main_win.destroy()
    os.chdir("data")
    sys.path.append(os.getcwd())
    runpy.run_path(file)


def save_settings(exit):
    """Write all of the variables to settings.pkl."""
    # (well right now it just prints them)
    print("Gamepad:", gamepad_connected.get())
    print("Width:", screen_width.get())
    print("Height:", screen_height.get())
    print("ID:", gamepad_id.get())
    print("Deadzone:", deadzone.get())
    print("X:", axis_x.get())
    print("Y:", axis_y.get())
    print("Dpad ID:", hat_id.get())
    print("FPS shown?:", show_fps.get())
    print()
    if exit:
        sett_win.withdraw()


# Define the image, buttons, and other stuff.
# Main window
title = Image.open("data/assets/logo.png")
title = title.resize((400, 225), resample=Image.BICUBIC)
title = ImageTk.PhotoImage(title)
logo = ttk.Label(main_win, image=title)
logo.image = title  # necessary in case the image gets garbage-collected
but_play = ttk.Button(main_win, text="Play Bullet Heck!", command=launch)
but_settings = ttk.Button(main_win, text="Settings",
                          command=sett_win.deiconify)
# Settings window
notebook = ttk.Notebook(sett_win)
page1 = tk.Frame(sett_win)
page1.columnconfigure(0, weight=1)  # fills the frame width
notebook.add(page1, text="General settings")
cb1 = ttk.Checkbutton(page1, text="I have a gamepad connected",
                      var=gamepad_connected)
en1_lb = ttk.Label(page1, text="Window resolution (width x height):")
en1 = ttk.Entry(page1, textvar=screen_width, width=5)
en2_lb = ttk.Label(page1, text="x")
en2 = ttk.Entry(page1, textvar=screen_height, width=5)

page2 = tk.Frame(sett_win)
page2.columnconfigure(0, weight=1)
notebook.add(page2, text="Gamepad settings")
pg2_lb = ttk.Label(page2, text="Only change these if you need to.")
en3 = ttk.Entry(page2, textvar=gamepad_id)
en3_lb = ttk.Label(page2, text="Gamepad ID:")
en4 = ttk.Entry(page2, textvar=deadzone)
en4_lb = ttk.Label(page2, text="Deadzone:")
en5 = ttk.Entry(page2, textvar=axis_x)
en5_lb = ttk.Label(page2, text="X axis ID:")
en6 = ttk.Entry(page2, textvar=axis_y)
en6_lb = ttk.Label(page2, text="Y axis ID:")
en7 = ttk.Entry(page2, textvar=hat_id)
en7_lb = ttk.Label(page2, text="Hat (dpad) ID:")
but_gptest = ttk.Button(page2, text="Controller Test",
                        command=lambda: launch("controllertest.py"))

page3 = tk.Frame(sett_win)
page3.columnconfigure(0, weight=1)
notebook.add(page3, text="Performance settings")
pg3_lb = ttk.Label(page3, text="Only change these if you need to.")
cb2 = ttk.Checkbutton(page3, text="Show FPS in console", var=show_fps)

savesettings = ttk.Button(sett_win, text="Save settings",
                          command=lambda: save_settings(False))
exit = ttk.Button(sett_win, text="Exit", command=sett_win.withdraw)
saveandexit = ttk.Button(sett_win, text="Save and Exit",
                         command=lambda: save_settings(True))
# Draw all the stuff.
logo.pack()
but_play.pack(fill=tk.X)
but_settings.pack(fill=tk.X)
# Settings window
notebook.grid(columnspan=3)
savesettings.grid(row=1, sticky="we")
exit.grid(row=1, column=1, sticky="we")
saveandexit.grid(row=1, column=2, sticky="we")

cb1.grid(columnspan=4)
en1_lb.grid(row=1)
en1.grid(row=1, column=1)
en2_lb.grid(row=1, column=2)
en2.grid(row=1, column=3)

pg2_lb.grid(columnspan=2)
en3_lb.grid(row=1, sticky="e")
en3.grid(row=1, column=1)
en4_lb.grid(row=2, sticky="e")
en4.grid(row=2, column=1)
en5_lb.grid(row=3, sticky="e")
en5.grid(row=3, column=1)
en6_lb.grid(row=4, sticky="e")
en6.grid(row=4, column=1)
en7_lb.grid(row=5, sticky="e")
en7.grid(row=5, column=1)
but_gptest.grid(row=6, columnspan=2, sticky="we")

pg3_lb.grid(columnspan=2)
cb2.grid(row=1)

# Hide the settings window by default.
# sett_win.withdraw()
# Main loops
main_win.mainloop()
sett_win.mainloop()
