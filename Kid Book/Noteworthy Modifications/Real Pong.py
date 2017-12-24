import tkinter
from tkinter import messagebox  # correction given on book's website
import time
canvasWidth = 750
canvasHeight = 500
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight, bg="dodgerblue4")
canvas.pack()
bat1 = canvas.create_rectangle(0, 0, 40, 10, fill="dark turquoise")
bat2 = canvas.create_rectangle(0, 0, 40, 10, fill="dark turquoise")
ball = canvas.create_oval(0, 0, 10, 10, fill="deep pink")
windowOpen = True
score1 = 0
score2 = 0
def main_loop():
    while windowOpen is True:
        move_bat1()
        move_bat2()
        move_ball()
        window.update()
        time.sleep(1 / 60)  # default is 0.02 (50fps) - warning: tied to speed
        if windowOpen is True:
            check_game_over()
leftPressed = 0
rightPressed = 0
aPressed = 0
dPressed = 0
def on_key_press(event):
    global leftPressed, rightPressed, aPressed, dPressed
    if event.keysym == "Left":
        leftPressed = 1
    elif event.keysym == "Right":
        rightPressed = 1
    elif event.keysym == "a":
        aPressed = 1
    elif event.keysym == "d":
        dPressed = 1
def on_key_release(event):
    global leftPressed, rightPressed, aPressed, dPressed
    if event.keysym == "Left":
        leftPressed = 0
    elif event.keysym == "Right":
        rightPressed = 0
    elif event.keysym == "a":
        aPressed = 0
    elif event.keysym == "d":
        dPressed = 0
batSpeed = 6
def move_bat1():
    bat1Move = batSpeed * rightPressed - batSpeed * leftPressed
    (bat1Left, bat1Top, bat1Right, bat1Bottom) = canvas.coords(bat1)
    if (bat1Left > 0 or bat1Move > 0) and (bat1Right < canvasWidth or bat1Move < 0):
        canvas.move(bat1, bat1Move, 0)
def move_bat2():
    bat2Move = batSpeed * dPressed - batSpeed * aPressed
    (bat2Left, bat2Top, bat2Right, bat2Bottom) = canvas.coords(bat2)
    if (bat2Left > 0 or bat2Move > 0) and (bat2Right < canvasWidth or bat2Move < 0):
        canvas.move(bat2, bat2Move, 0)
ballMoveX = 4
ballMoveY = -5
setBat1Top = canvasHeight - 40
setBat1Bottom = canvasHeight - 30
setBat2Top = canvasHeight - 460
setBat2Bottom = canvasHeight - 450
def move_ball():
    global ballMoveX, ballMoveY, score
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballMoveX > 0 and ballRight > canvasWidth:
        ballMoveX = -ballMoveX
    if ballMoveX < 0 and ballLeft < 0:
        ballMoveX = -ballMoveX
    # if ballMoveY < 0 and ballTop < 0: (bouncing)
        # ballMoveY = -ballMoveY
    if ballMoveY > 0 and ballBottom > setBat1Top and ballBottom < setBat1Bottom:
        (bat1Left, bat1Top, bat1Right, bat1Bottom) = canvas.coords(bat1)
        if ballRight > bat1Left and ballLeft < bat1Right:
            ballMoveY = -ballMoveY
    if ballMoveY < 0 and ballTop > setBat2Top and ballTop < setBat2Bottom:
        (bat2Left, bat2Top, bat2Right, bat2Bottom) = canvas.coords(bat2)
        if ballRight > bat2Left and ballLeft < bat2Right:
            ballMoveY = -ballMoveY
    canvas.move(ball, ballMoveX, ballMoveY)
def check_game_over():
    global score1, score2
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballTop > canvasHeight:
        score2 = score2 + 1
        p2Scores = messagebox.askyesno(message="1 point to Player 2!\nScores are:\n%s for player 1 and %s for player 2!\nContinue?" % (score1, score2))
        if p2Scores is True:
            reset()
        else:
            close()
    if ballBottom < 0:
        score1 = score1 + 1
        p1Scores = messagebox.askyesno(message="1 point to Player 1!\nScores are:\n%s for player 1 and %s for player 2!\nContinue?" % (score1, score2))
        if p1Scores is True:
            reset()
        else:
            close()
def close():
    global windowOpen
    windowOpen = False
    window.destroy()
def reset():
    global leftPressed, rightPressed, aPressed, dPressed
    global ballMoveX, ballMoveY
    leftPressed = 0
    rightPressed = 0
    aPressed = 0
    dPressed = 0
    ballMoveX = 4
    ballMoveY = -5
    canvas.coords(bat1, 10, setBat1Top, 70, setBat1Bottom)  # default was 10, 50
    canvas.coords(bat2, 10, setBat2Top, 70, setBat2Bottom)
    canvas.coords(ball, 20, setBat1Top - 10, 30, setBat1Top)
window.protocol("WM_DELETE_WINDOW", close)
window.bind("<KeyPress>", on_key_press)
window.bind("<KeyRelease>", on_key_release)
reset()
main_loop()
