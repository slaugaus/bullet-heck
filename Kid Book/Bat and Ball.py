import tkinter
from tkinter import messagebox  # correction given on book's website
import time
import random
canvasWidth = 750
canvasHeight = 500
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight, bg="dodgerblue4")
canvas.pack()
bat = canvas.create_rectangle(0, 0, 40, 10, fill="dark turquoise")  # bat width is the second number in line 77
ball = canvas.create_oval(0, 0, 10, 10, fill="deep pink")
windowOpen = True
score = 0
def main_loop():
    while windowOpen is True:
        move_bat()
        move_ball()
        window.update()
        time.sleep(1 / 60)  # default is 0.02 (50fps) - warning: tied to speed
        if windowOpen is True:
            check_game_over()
leftPressed = 0
rightPressed = 0
def on_key_press(event):
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 1
    elif event.keysym == "Right":
        rightPressed = 1
def on_key_release(event):
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 0
    elif event.keysym == "Right":
        rightPressed = 0
batSpeed = 6
def move_bat():
    batMove = batSpeed * rightPressed - batSpeed * leftPressed
    (batLeft, batTop, batRight, batBottom) = canvas.coords(bat)
    if (batLeft > 0 or batMove > 0) and (batRight < canvasWidth or batMove < 0):
        canvas.move(bat, batMove, 0)
ballMoveX = 4
ballMoveY = -4
setBatTop = canvasHeight - 40
setBatBottom = canvasHeight - 30
def move_ball():
    global ballMoveX, ballMoveY, score
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballMoveX > 0 and ballRight > canvasWidth:
        ballMoveX = -ballMoveX
    if ballMoveX < 0 and ballLeft < 0:
        ballMoveX = -ballMoveX
    if ballMoveY < 0 and ballTop < 0:
        ballMoveY = -ballMoveY
    if ballMoveY > 0 and ballBottom > setBatTop and ballBottom < setBatBottom:
        (batLeft, batTop, batRight, batBottom) = canvas.coords(bat)
        if ballRight > batLeft and ballLeft < batRight:
            ballMoveY = -ballMoveY
            score = score + 1
            print(score)
    canvas.move(ball, ballMoveX, ballMoveY)
def check_game_over():
    global score
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballTop > canvasHeight:
        playAgain = messagebox.askyesno(message="You lost! Want to play again?\nYour score was: %s" % score, icon="error", title="Oh no!")
        if playAgain is True:
            reset()
        else:
            close()
def close():
    global windowOpen
    windowOpen = False
    window.destroy()
def reset():
    global leftPressed, rightPressed
    global ballMoveX, ballMoveY
    global score
    leftPressed = 0
    rightPressed = 0
    ballMoveX = 4
    ballMoveY = -4
    score = 0
    canvas.coords(bat, 10, setBatTop, 70, setBatBottom)  # default was 10, 50
    canvas.coords(ball, 20, setBatTop - 10, 30, setBatTop)
window.protocol("WM_DELETE_WINDOW", close)
window.bind("<KeyPress>", on_key_press)
window.bind("<KeyRelease>", on_key_release)
reset()
main_loop()
