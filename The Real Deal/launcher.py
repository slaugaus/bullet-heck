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

main_window = tk.Tk()
main_window.title("Bullet Heck! Launcher")
settings_window = tk.Tk()
settings_window.title("Settings")


def launch():
    main_window.destroy()
    os.chdir("data")
    sys.path.append(os.getcwd())
    runpy.run_path("BulletHeck.py")


# Defining all the stuff
# PIL is weird.
title = Image.open("data/assets/images/logo.png")
title = title.resize((400, 225), resample=Image.BICUBIC)
title = ImageTk.PhotoImage(title)
logo = ttk.Label(main_window, image=title)
logo.image = title  # necessary in case the image gets garbage-collected
but_play = ttk.Button(main_window, text="Play Bullet Heck!",
                      command=launch)
but_settings = ttk.Button(main_window, text="Settings")
# Drawing all the stuff
logo.pack()
but_play.pack(fill=tk.X)
but_settings.pack(fill=tk.X)

main_window.mainloop()
settings_window.mainloop()
