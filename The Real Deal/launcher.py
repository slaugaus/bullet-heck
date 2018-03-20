# Warning: Spaghetti code below.
# Actual necessary libs
import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import runpy
import sys
import os
from PIL import Image, ImageTk
# Libs used by the target file (needed for compilation)
import pygame
import random
# Create and/or load settings.pickle
try:
    file = open("settings.pickle", mode="r+b")
    vars_to_load = pickle.load(file)
    # If the settings say to skip the launcher, do so.
    if vars_to_load[10]:
        os.chdir("data")
        sys.path.append(os.getcwd())
        runpy.run_path("BulletHeck.py")
    else:
        file = open("settings.pickle", mode="w+b")
        settings_exist = True
except (FileNotFoundError, EOFError):
    file = open("settings.pickle", mode="w+b")
    file = open("settings.pickle", mode="r+b")
    settings_exist = False
# Define the windows.
main_win = tk.Tk()
main_win.title("Bullet Heck! Launcher")
main_win.resizable(False, False)
sett_win = tk.Toplevel()
sett_win.title("Settings")
sett_win.protocol("WM_DELETE_WINDOW", sett_win.withdraw)
sett_win.resizable(False, False)
# Variables that will be written to settings
gamepad_connected = tk.BooleanVar(sett_win)
screen_res = tk.StringVar(sett_win)
gamepad_id = tk.IntVar(sett_win)
deadzone = tk.DoubleVar(sett_win)
axis_x = tk.IntVar(sett_win)
axis_y = tk.IntVar(sett_win)
hat_id = tk.IntVar(sett_win)
but_A = tk.IntVar(sett_win)
but_B = tk.IntVar(sett_win)
show_fps = tk.BooleanVar(sett_win)
skip_launcher = tk.BooleanVar(sett_win)
autofire = tk.BooleanVar(sett_win)

var_list = [gamepad_connected, screen_res, gamepad_id, deadzone, axis_x,
            axis_y, hat_id, but_A, but_B, show_fps, skip_launcher, autofire]


def reset_settings(confirm):
    """Reset the settings to the defaults, possibly asking to confirm."""
    if not confirm:
        gamepad_connected.set(False)
        screen_res.set("1600 x 900")
        gamepad_id.set(0)
        deadzone.set(0.2)
        axis_x.set(0)
        axis_y.set(1)
        hat_id.set(0)
        but_A.set(0)
        but_B.set(1)
        show_fps.set(False)
        skip_launcher.set(False)
        autofire.set(False)
    else:
        confirm = messagebox.askokcancel(message="Are you sure?")
        if confirm:
            reset_settings(False)


# Set the default values of the variables
if not settings_exist:
    reset_settings(False)
else:
    # Copy the loaded values to the Tkinter variables.
    for var in var_list:
        var.set(vars_to_load[var_list.index(var)])


def warn_res():
    """Throw a warning window if the resolution is too high."""
    if int(screen_res.get().split()[0]) > main_win.winfo_screenwidth():
        messagebox.showwarning(title="Warning!",
                               message=("Your screen is smaller than "
                                        "the recommended value!\n"
                                        "Set \"Window resolution\" to "
                                        "something lower.\nNote that this "
                                        "will make the game harder."))
        return False
    else:
        return True


def launch(target="BulletHeck.py"):
    """Run another .py file, which should be BulletHeck.py."""
    if target == "BulletHeck.py":
        if warn_res() is True:
            sett_win.destroy()
            main_win.destroy()
            save_settings(False)
            os.chdir("data")
            sys.path.append(os.getcwd())
            runpy.run_path(target)
    else:
        runpy.run_path(target)


def save_settings(exit):
    """Write all of the variables to settings.pickle."""
    global file
    vars_to_save = [gamepad_connected.get(), screen_res.get(),
                    gamepad_id.get(), deadzone.get(), axis_x.get(),
                    axis_y.get(), hat_id.get(), but_A.get(), but_B.get(),
                    show_fps.get(), skip_launcher.get(), autofire.get()]
    pickle.dump(vars_to_save, file)
    # Close and reopen the file so pickle can actually modify it.
    file.close()
    file = open("settings.pickle", mode="r+b")
    if exit:
        sett_win.withdraw()


def show_credits():
    messagebox.showinfo(title="Credits",
                        message="Sound effects obtained from www.zapsplat.com")


def show_skip_msg():
    messagebox.showinfo(message=("To see the launcher again, "
                                 "delete settings.pickle.\n"
                                 "This will also reset your settings."))


# Define all of the widgets.
# Main window
title = Image.open("data/assets/logo.png")
title = title.resize((400, 225), resample=Image.BICUBIC)
title = ImageTk.PhotoImage(title)
logo = ttk.Label(main_win, image=title)
logo.image = title  # necessary in case the image gets garbage-collected
but_play = ttk.Button(main_win, text="Play Bullet Heck!", command=launch)
but_settings = ttk.Button(main_win, text="Settings",
                          command=sett_win.deiconify)
but_credits = ttk.Button(main_win, text="Credits", command=show_credits)
# Settings window
notebook = ttk.Notebook(sett_win)
page1 = tk.Frame(sett_win)
page1.columnconfigure(0, weight=1)  # fills the frame width
notebook.add(page1, text="General settings")
cb1 = ttk.Checkbutton(page1, text="I have a gamepad connected",
                      var=gamepad_connected)
cb2 = ttk.Checkbutton(page1, text="Show framerate in console", var=show_fps)
cb3 = ttk.Checkbutton(page1, text="Don't show the launcher again",
                      var=skip_launcher, command=show_skip_msg)
cb4 = ttk.Checkbutton(page1, text="Fire bullets automatically", var=autofire)
combobox1_lb = ttk.Label(page1, text="Window resolution:")
combobox1 = ttk.Combobox(page1, textvar=screen_res, state="readonly",
                         values=["1600 x 900", "1366 x 768",
                                 "1280 x 720", "1152 x 648"])

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
en7_lb = ttk.Label(page2, text="Hat (D-pad) ID:")
en8 = ttk.Entry(page2, textvar=but_A)
en8_lb = ttk.Label(page2, text="ID of A (down) Button:")
en9 = ttk.Entry(page2, textvar=but_B)
en9_lb = ttk.Label(page2, text="ID of B (right) Button:")
but_gptest = ttk.Button(page2, text="Controller Test",
                        command=lambda: launch("controllertest.py"))

save = ttk.Button(sett_win, text="Save settings",
                  command=lambda: save_settings(False))
reset = ttk.Button(sett_win, text="Reset settings",
                   command=lambda: reset_settings(True))
saveandexit = ttk.Button(sett_win, text="Save and Exit",
                         command=lambda: save_settings(True))
# Draw all the stuff.
logo.pack()
but_play.pack(fill=tk.X)
but_settings.pack(fill=tk.X)
but_credits.pack(fill=tk.X)
# Settings window
notebook.grid(columnspan=3)
save.grid(row=1, sticky="we")
reset.grid(row=1, column=1, sticky="we")
saveandexit.grid(row=1, column=2, sticky="we")

cb1.grid(columnspan=2)
cb2.grid(row=1, columnspan=2)
cb3.grid(row=2, columnspan=2)
cb4.grid(row=3, columnspan=2)
combobox1_lb.grid(row=4)
combobox1.grid(row=4, column=1)

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
en8_lb.grid(row=6, sticky="e")
en8.grid(row=6, column=1)
en9_lb.grid(row=7, sticky="e")
en9.grid(row=7, column=1)
but_gptest.grid(row=8, columnspan=2, sticky="we")

# Hide the settings window by default.
sett_win.withdraw()
# Check resolution.
warn_res()
# Main loops
main_win.mainloop()
sett_win.mainloop()
