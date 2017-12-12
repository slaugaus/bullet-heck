import tkinter
print("To draw, hold LMB and move it. Wow!")
print("To change colors, click on one of them. Amazing!")
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=750, height=500, bg="white")
canvas.pack()
lastX, lastY = 0, 0
color = "black"
def store_position(event):
    global lastX, lastY
    lastX = event.x
    lastY = event.y
def on_click(event):
    store_position(event)
def on_drag(event):
    canvas.create_line(lastX, lastY, event.x, event.y, fill=color, width=3)
    store_position(event)
canvas.bind("<Button-1>", on_click)
canvas.bind("<B1-Motion>", on_drag)
red_id = canvas.create_rectangle(10, 10, 30, 30, fill="red")
blue_id = canvas.create_rectangle(10, 35, 30, 55, fill="blue")
black_id = canvas.create_rectangle(10, 60, 30, 80, fill="black")
white_id = canvas.create_rectangle(10, 85, 30, 105, fill="white")
def set_color_red(event):
    global color
    color = "red"
def set_color_blue(event):
    global color
    color = "blue"
def set_color_black(event):
    global color
    color = "black"
def set_color_white(event):
    global color
    color = "white"
canvas.tag_bind(red_id, "<Button-1>", set_color_red)
canvas.tag_bind(blue_id, "<Button-1>", set_color_blue)
canvas.tag_bind(black_id, "<Button-1>", set_color_black)
canvas.tag_bind(white_id, "<Button-1>", set_color_white)
window.mainloop()
