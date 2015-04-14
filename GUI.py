#Feb-07-2014
#Developed by
# Daniel Lucas Thompson & Bikramjit Banerjee
# School of Computing
# The University of Southern Mississippi

#License
#====================================================================
#This is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with TraceGen.  If not, see <http://www.gnu.org/licenses/>. 
#===================================================================

import Tkinter as tk
from Boards import *


class gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('526x585')
        self.window.title("Strimko by Resolution")
        self.window.resizable(width=tk.FALSE, height=tk.FALSE)

        #window and drawing variables
        self.paddingx = 45
        self.paddingy = 45
        self.spacerx = 8
        self.spacery = 10
        self.topSpacerx = 7
        self.topSpacery = 28
        self.sideSpacerx = 25
        self.sideSpacery = 10
        self.gameSize = 5
        self.radius = 25
        self.colors = ['#FF0000', '#FF8C00', '#FFFF00', '#008000', '#0000FF', '#800080', '#FF69B4']
        self.nodesXY = {}

        #canvases to display the nodes and labels
        canvasFrame = tk.Frame(self.window)#, borderwidth=2, relief=tk.GROOVE)
        self.topLabels = tk.Canvas(canvasFrame, width=460, height=50, borderwidth=2, relief=tk.GROOVE)
        self.topLabels.grid(row=0, column=1)#, columnspan=3)
        self.sideLabels = tk.Canvas(canvasFrame, width=50, height=460, borderwidth=2, relief=tk.GROOVE)
        self.sideLabels.grid(row=1, column=0)
        self.canvas = tk.Canvas(canvasFrame, width=460, height=460, borderwidth=2, relief=tk.GROOVE)
        self.canvas.grid(row=1, column=1)#, columnspan=3)
        canvasFrame.grid(row=0, column=0)

        #Menu bar to select game options
        menuBar = tk.Menu(self.window)
        gameMenu = tk.Menu(menuBar, tearoff=0)

        #4x4 game boards menu
        submenu4 = tk.Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="4x4 Boards", menu=submenu4)
        submenu4.add_command(label="Board #1 (Easy)", command=(lambda:self.changeboard("4_1")))
        submenu4.add_command(label="Board #2 (Easy)", command=(lambda:self.changeboard("4_2")))
        submenu4.add_command(label="Board #3 (Easy)", command=(lambda:self.changeboard("4_3")))
        submenu4.add_command(label="Board #4 (Easy)", command=(lambda:self.changeboard("4_4")))
        submenu4.add_command(label="Board #5 (Easy)", command=(lambda:self.changeboard("4_5")))

        #5x5 game boards menu
        submenu5 = tk.Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="5x5 Boards", menu=submenu5)
        submenu5.add_command(label="Board #6 (Easy)", command=(lambda:self.changeboard("5_6")))
        submenu5.add_command(label="Board #4 (Easy)", command=(lambda:self.changeboard("5_4")))
        submenu5.add_command(label="Board #2 (Medium)", command=(lambda:self.changeboard("5_2")))
        submenu5.add_command(label="Board #3 (Medium)", command=(lambda:self.changeboard("5_3")))
        submenu5.add_command(label="Board #5 (Medium)", command=(lambda:self.changeboard("5_5")))
        submenu5.add_command(label="Board #7 (Medium)", command=(lambda:self.changeboard("5_7")))
        submenu5.add_command(label="Board #8 (Medium)", command=(lambda:self.changeboard("5_8")))
        submenu5.add_command(label="Board #9 (Medium)", command=(lambda:self.changeboard("5_9")))
        submenu5.add_command(label="Board #10 (Medium) Unsolved", command=(lambda:self.changeboard("5_10")))
        submenu5.add_command(label="Board #1 (Hard)", command=(lambda:self.changeboard("5_1")))

        #6x6 game boards menu
        submenu6 = tk.Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="6x6 Boards", menu=submenu6)
        submenu6.add_command(label="Board #1 (Hard)", command=(lambda:self.changeboard("6_1")))
        submenu6.add_command(label="Board #2 (Hard)", command=(lambda:self.changeboard("6_2")))
        submenu6.add_command(label="Board #3 (Hard)", command=(lambda:self.changeboard("6_3")))
        submenu6.add_command(label="Board #4 (Hard) Unsolved", command=(lambda:self.changeboard("6_4")))
        submenu6.add_command(label="Board #5 (Hard) Unsolved", command=(lambda:self.changeboard("6_5")))

        #7x7 game boards menu
        submenu7 = tk.Menu(gameMenu, tearoff=0)
        gameMenu.add_cascade(label="7x7 Boards", menu=submenu7)
        submenu7.add_command(label="Board #1 (Hard)", command=(lambda:self.changeboard("7_1")))
        submenu7.add_command(label="Board #2 (Hard)", command=(lambda:self.changeboard("7_2")))
        submenu7.add_command(label="Board #3 (Hard)", command=(lambda:self.changeboard("7_3")))

        gameMenu.add_separator()
        gameMenu.add_command(label="Exit", command=(lambda:sys.exit(0)))
        menuBar.add_cascade(label="Game Menu", menu=gameMenu)
        self.window.config(menu=menuBar)

        #buttons for next, solve, and reset
        buttonFrame = tk.Frame(self.window, borderwidth=2, relief=tk.GROOVE)
        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)
        solve = tk.Button(buttonFrame, height=2, text="Reset", command=self.reset).grid(row=1, column=0, sticky="nsew")
        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)
        reset = tk.Button(buttonFrame, height=2, text="Solve", command=self.solve).grid(row=1, column=1, sticky="nsew")
        tk.Grid.rowconfigure(buttonFrame, 1, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 1, weight=1)
        next = tk.Button(buttonFrame, height=2, text="Next", command=self.next).grid(row=1, column=2, sticky="nsew")
        tk.Grid.rowconfigure(buttonFrame, 2, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 2, weight=1)
        buttonFrame.grid(row=1,column=0,sticky="nsew")

        #game data
        self.cellLock = thread.allocate_lock()
        self.currentCell = None
        self.prevCell = None
        self.size = 5 #default 5x5 starting board
        self.boardID = "5_1" #default starting board
        self.game = Board(self.size, self, self.boardID)
        self.board = self.game.board
        self.setGameSize(self.size)

        #run the game
        self.drawBoard()
        self.window.mainloop()

    def solve(self):
        #Action for the solve button
        self.game.solveGame()

    def next(self):
        #Action for the next button
        self.game.pauseGame()

    def reset(self):
        #Action for the reset button
        self.game.killThread = True
        self.game = Board(self.size, self, self.boardID)
        self.board = self.game.board
        self.prevCell = None
        self.currentCell = None
        self.drawBoard()

    def changeboard(self, id):
        #Changes the board when a new one is selected in the menu
        self.boardID = id
        self.size = int(id[0])
        self.setGameSize(self.size)
        self.reset()

    def drawLabels(self):
        #draw the GUI label info
        self.sideLabels.delete('all')
        self.topLabels.delete('all')

        #Top markers for canvas
        x,y = self.topSpacerx, self.topSpacery
        for i in range(self.gameSize):
            x += self.paddingx
            self.topLabels.create_text((x,y), text="C" + str(i+1))
            x += self.paddingx

        #Side markers for canvas
        x,y = self.sideSpacerx, self.sideSpacery
        for i in range(self.gameSize):
            y += self.paddingy
            self.sideLabels.create_text((x,y), text="R" + str(i+1))
            y += self.paddingy

    def setGameSize(self, n):
        #starts a new board size
        #different GUI variables to adjust the GUI depending on board size
        self.gameSize = n
        if n == 4:
            self.size = 4
            self.paddingx = 52
            self.paddingy = 52
            self.spacerx = 8
            self.spacery = 10
            self.topSpacerx = 7
            self.topSpacery = 28
            self.sideSpacerx = 25
            self.sideSpacery = 10
        elif n == 5:
            self.size = 5
            self.paddingx = 45
            self.paddingy = 45
            self.spacerx = 8
            self.spacery = 10
            self.topSpacerx = 7
            self.topSpacery = 28
            self.sideSpacerx = 25
            self.sideSpacery = 10
        elif n == 6:
            self.size = 6
            self.paddingx = 38
            self.paddingy = 38
            self.spacerx = 6
            self.spacery = 6
            self.topSpacerx = 7
            self.topSpacery = 28
            self.sideSpacerx = 25
            self.sideSpacery = 5
        elif n == 7:
            self.size = 7
            self.paddingx = 33
            self.paddingy = 33
            self.spacerx = 3
            self.spacery = 2
            self.topSpacerx = 4
            self.topSpacery = 28
            self.sideSpacerx = 25
            self.sideSpacery = 3
        self.drawBoard()

    def drawBoard(self):
        #calls all the separate draw functions to construct a board
        self.canvas.delete('all')
        self.drawLabels()
        self.drawCells()
        self.drawChains()
        self.drawCells()
        self.writeNumbers()
        self.game.runGame()

    def drawCells(self):
        #draws the circles for each cell
        x = self.spacerx
        y = self.spacery
        for i in range(self.size):
            y += self.paddingy
            for j in range(self.size):
                x += self.paddingx
                self.nodesXY[(j+1, i+1)] = (x, y)
                self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, width=0, fill="lightgrey")
                x += self.paddingx
            y += self.paddingy
            x = self.spacerx

    def drawChains(self):
        #draws the colored chains that connects the cells
        chains = self.board[1]
        for i, c in enumerate(chains):
            prev = None
            for n in c:
                x = self.nodesXY[n][0]
                y = self.nodesXY[n][1]
                self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, width=5, outline=self.colors[i])
                if prev != None:
                    px = self.nodesXY[prev][0]
                    py = self.nodesXY[prev][1]
                    self.canvas.create_line(px, py, x, y, width=5, fill=self.colors[i])
                    self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, width=5, outline=self.colors[i])
                prev = n

    def writeNumbers(self):
        #writes all the solved numbers onto the board
        self.game.boardLock.acquire()
        answers = copy.deepcopy(self.board[0])
        self.game.boardLock.release()
        self.cellLock.acquire()
        #highlight the currently solved cell
        if self.currentCell !=  None:
            x = self.nodesXY[self.currentCell][0]
            y = self.nodesXY[self.currentCell][1]
            #erase the previous highlighted cell
            if self.prevCell != None:
                xp = self.nodesXY[self.prevCell][0]
                yp = self.nodesXY[self.prevCell][1]
                self.canvas.create_oval(xp-self.radius, yp-self.radius, xp+self.radius, yp+self.radius, width=0, fill="lightgrey")
            if self.game.solve != True:
                #only highlight cells when the next button is used
                self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, width=0, fill="green")
            self.prevCell = self.currentCell
        #write the solved number in each solved cell
        for i, row in enumerate(answers):
            for j, n in enumerate(row):
                node = (j+1, i+1)
                x = self.nodesXY[node][0]
                y = self.nodesXY[node][1]
                if n == 0:
                   continue
                self.canvas.create_text((x,y), text=str(n), font=("Purisa", 12))
        self.cellLock.release()


if __name__ == "__main__":
    strimko = gui()
