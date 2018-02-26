# Warning: Spaghetti code below.
# Actual necessary libs
import tkinter as tk
from tkinter import ttk
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


def launch():
    # Run the game.
    sett_win.destroy()
    main_win.destroy()
    os.chdir("data")
    sys.path.append(os.getcwd())
    runpy.run_path("BulletHeck.py")


# Define the images and buttons.
title = Image.open("data/assets/logo.png")
title = title.resize((400, 225), resample=Image.BICUBIC)
title = ImageTk.PhotoImage(title)
logo = ttk.Label(main_win, image=title)
logo.image = title  # necessary in case the image gets garbage-collected
but_play = ttk.Button(main_win, text="Play Bullet Heck!", command=launch)
but_settings = ttk.Button(main_win, text="Settings",
                          command=lambda: sett_win.deiconify())
notebook = ttk.Notebook(sett_win)
test1 = ttk.Label(sett_win, image=title)
frame = tk.Frame(sett_win)
test2 = ttk.Button(frame, text="Play Bullet Heck!", command=launch)
notebook.add(test1, text="pic")
notebook.add(frame, text="buttons")
# Draw all the stuff.
logo.pack()
but_play.pack(fill=tk.X)
but_settings.pack(fill=tk.X)
notebook.pack()
test2.pack()
# Hide the settings window.
sett_win.withdraw()

main_win.mainloop()
sett_win.mainloop()
