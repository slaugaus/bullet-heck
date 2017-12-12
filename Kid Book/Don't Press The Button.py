import tkinter
window = tkinter.Tk()
button = tkinter.Button(window, text="Please don't press this button.", width=40)
button.pack(padx=10, pady=10)
clickCount = 0
def onClick(event):
    global clickCount
    clickCount = clickCount + 1
    if clickCount == 1:
        button.configure(text="No, really, don't press it.")
    elif clickCount == 2:
        button.configure(text="Gah! Next time, no more button.")
    else:
        button.pack_forget()
button.bind("<ButtonRelease-1>", onClick)
window.mainloop()
