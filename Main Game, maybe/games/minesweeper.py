# "Minesweeper" is a better name anyway.
import tkinter
import random
gameOver = False
score = 0
squaresToClear = 0
def play_minesweeper():
    create_minefield(minefield)
    window = tkinter.Tk()
    layout_window(window)
    window.mainloop()
minefield = []
def create_minefield(minefield):
    global squaresToClear
    for row in range(0, 10):
        rowList = []
        for column in range(0, 10):
            if random.randint(1, 100) < 20:
                rowList.append(1)
            else:
                rowList.append(0)
                squaresToClear = squaresToClear + 1
        minefield.append(rowList)
    printfield(minefield)
def printfield(minefield):
    print("Here's the solution, you cheater:")
    for rowList in minefield:
        print(rowList)
def layout_window(window):
    for rowNumber, rowList in enumerate(minefield):
        for columnNumber, columnEntry in enumerate(rowList):
            if random.randint(1, 100) < 25:
                square = tkinter.Label(window, text="    ", bg="darkgreen")
            elif random.randint(1, 100) > 75:
                square = tkinter.Label(window, text="    ", bg="seagreen")
            else:
                square = tkinter.Label(window, text="    ", bg="green")
            square.grid(row=rowNumber, column=columnNumber)
            square.bind("<Button-1>", on_click)
def on_click(event):
    global score
    global gameOver
    global squaresToClear
    square = event.widget
    row = int(square.grid_info()["row"])
    column = int(square.grid_info()["column"])
    currentText = square.cget("text")
    if gameOver is False:
        if minefield[row][column] == 1:
            gameOver = True
            square.config(bg="red")
            print("Game over! You hit a mine! :(")
            print("Your score was:", score)
        elif currentText == "    ":
            square.config(bg="brown")
            totalMines = 0
            if row < 9:
                if minefield[row + 1][column] == 1:
                    totalMines = totalMines + 1
            if row > 0:
                if minefield[row - 1][column] == 1:
                    totalMines = totalMines + 1
            if column > 0:
                if minefield[row][column - 1] == 1:
                    totalMines = totalMines + 1
            if column < 9:
                if minefield[row][column + 1] == 1:
                    totalMines = totalMines + 1
            if row > 0 and column > 0:
                if minefield[row - 1][column - 1] == 1:
                    totalMines = totalMines + 1
            if row < 9 and column > 0:
                if minefield[row + 1][column - 1] == 1:
                    totalMines = totalMines + 1
            if row > 0 and column < 9:
                if minefield[row - 1][column + 1] == 1:
                    totalMines = totalMines + 1
            if row < 9 and column < 9:
                if minefield[row + 1][column + 1] == 1:
                    totalMines = totalMines + 1
            square.config(text=" " + str(totalMines) + " ")
            squaresToClear = squaresToClear - 1
            score = score + 1
            if squaresToClear == 0:
                gameOver = True
                print("Yay, you found all of the safe squares!")
                print("Your score was:", score)
play_minesweeper()
