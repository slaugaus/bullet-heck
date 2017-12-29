import tkinter
import runpy
#  Games
pong = "games\pong.py"
mine = "games\minesweeper.py"

window = tkinter.Tk()
window.title("Austin's Game Collection Menu!")


def play(game):
    window.destroy()
    runpy.run_path(game)


title = tkinter.Label(window, font="TkDefaultFont 10 bold underline", text="Choose a game:")
title.pack(padx=125)
button1 = tkinter.Button(window, text="Pong in Tkinter", command=lambda: play(pong))
button1.pack(pady=1)
button2 = tkinter.Button(window, text="Minesweeper", command=lambda: play(mine))
button2.pack(pady=1)
window.mainloop()
