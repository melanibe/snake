from tkinter import *
import random as rd

class Application:
    def __init__(self):
        # init the main window
        self.root = Tk()
        self.root.title("Mel's snake")

        # init variables
        self.Direction = StringVar()
        self.Direction.set('Right')
        self.count = 1
        self.YourScore = IntVar()
        self.YourLevel = IntVar()
        self.YourLevel.set(1)
        
        # init top level frame
        self.ftop = Frame(self.root, width = 300, height= 300, bg='pink')
        self.ftop.pack(fill = BOTH, expand = 1)

        # add score
        self.f1 = Frame(self.ftop, bg='pink')
        self.f1.pack(side=TOP)
        self.f2 = Frame(self.f1, bg='pink')
        self.f2.pack(side=LEFT)
        self.score_title = Label(self.f2, text="Score", bg='pink', fg="white", font=("Helvetica", 16))
        self.score_title.grid(row=0, column=1, padx=5)
        self.score = Label(self.f2, textvariable=self.YourScore, bg='pink', fg="white", font=("Helvetica", 16) )
        self.score.grid(row=1, column=1, padx=5)

        # add level
        self.score_title = Label(self.f2, text="Level", bg='pink', fg="white", font=("Helvetica", 16))
        self.score_title.grid(row=0,column=2, padx=5)
        self.level = Label(self.f2, textvariable=self.YourLevel, bg='pink',  fg="white", font=("Helvetica", 16))
        self.level.grid(row=1, column=2, padx=5)

        # add the quit button
        self.quit = Button(self.f2, text="QUIT", bg='pink', fg= "white", highlightbackground='pink', \
			padx=3, pady=3, justify='center', bd= 5, command=self.root.destroy, font=("Helvetica", 16))
        self.quit.grid(row=0, column=5, rowspan=2, padx=(150,10))

        # create the game canvas 
        self.can = Canvas(self.ftop, width=300, height= 300)
        self.can.bind_all('<KeyPress>', self.changeDirection)
        self.can.pack(padx=10, pady=10)

        # init the first bonus
        self.drawBonus()

        # initialize the snake
        self.snake = [self.can.create_oval(140,140,150,150, fill='orange')]
        self.speed = 500
        self.mySnakeMove()

    def drawBonus(self):
        """ 
        Draw a random bonus square.
        """
        x0, y0 = (rd.randrange(10,280,10), rd.randrange(10,280,10))
        self.bonus = self.can.create_rectangle(x0, y0, x0+10, y0+10, fill = 'red')
        self.bonus_coords  = (x0, y0, x0+10, y0+10) 

    def oneSingleSnakeMove(self):
        """
        Helper for a defining the moving direction of the snake
        """
        direction = self.Direction.get()
        for i in range (len(self.snake)-1,0,-1):
            x0, y0, x1, y1 = self.can.coords(self.snake[i-1])
            self.can.coords(self.snake[i],x0, y0, x1, y1)   
        if direction == 'Up' :
            self.can.move(self.snake[0],0,-10)
        elif direction == 'Down':
            self.can.move(self.snake[0],0,10)
        elif direction == 'Left':
            self.can.move(self.snake[0],-10,0)
        elif direction == 'Right':
            self.can.move(self.snake[0], 10, 0)

    def getNextCoordinates(self):
        """
        Get the coordinates reached after the current move of the snake.
        """
        direction = self.Direction.get()
        x0, y0, x1, y1 = self.can.coords(self.snake[0])
        if direction == 'Up' :
            return(x0, y0-10, x1, y1-10) 
        elif direction == 'Down':
            return(x0, y0+10, x1, y1+10)
        elif direction == 'Left':
            return(x0-10,y0,x1-10,y1)
        elif direction == 'Right':
            return(x0+10,y0,x1+10,y1)

    def touchedSnake(self):
        """
        Check if the current move leads to touching another part of the snake
        """
        r = False
        for i in range(1,len(self.snake)):
            if r:
                break
            else:
                r = (self.can.coords(self.snake[i])==self.can.coords(self.snake[0]))
        return r

    def nextTouchBonus(self):
        """ Check if you are touching the bonus
        """
        r=False
        a, b, c, d = self.bonus_coords
        x0, y0, x1, y1 = self.getNextCoordinates()
        r = (((a == x0) and (x1==c)) and (y0==b and y1==d))
        return(r)

    def changeDirection(self, event):
        """ Get the changes of direction.
        """
        key = event.keysym
        self.Direction.set(key)

    def nextOutOfScreen(self):
        """ Check if you're going out of the screen
        """
        a,b,c,d = self.getNextCoordinates()
        r = (a < 0 or c>300 or b<0 or d > 300)
        return(r)

    def youLostScreen(self):
        """ This function defines the Game over screen.
        """
        self.can.destroy()
        self.can_lost = Canvas(self.ftop, width = 300, height= 300, bg='red')
        self.can_lost.pack()
        self.can_lost.create_text(145, 145, text='Game \n over', fill = 'white')

    def mySnakeMove(self):
        """ Main function for moving the snake.
        Makes single moves and checks the loosing conditions as well as
        the winning (touch bonus) conditions. 
        Increases speed and level if necessary
        """
        score = self.YourScore.get()
        level = self.YourLevel.get()
        a0, b0, a1, b1 = self.can.coords(self.snake[-1])
        # check the loosing conditions
        if (self.touchedSnake() or self.nextOutOfScreen()):
            self.youLostScreen()
        else:
            # check if you touch the bonus in this move
            if self.nextTouchBonus():
                # delete the touched bonus & add circle to snake
                s = self.can.create_oval(a0,b0,a1,b1, fill = 'pink')
                self.snake = self.snake +[s]
                self.can.delete(self.bonus)
                self.drawBonus()
                # increase the score
                self.YourScore.set(score + level*100)
                # increase the counter until next level
                self.count += 1
            # actually move the snake
            self.oneSingleSnakeMove()
            # every 5 touches increase the level and the speed
            if self.count==5:
                self.speed = self.speed // 2
                self.YourLevel.set(level+1)
                self.count = 1
            # repeat this after some time
            self.root.after(self.speed, self.mySnakeMove)


# Run your application.
if __name__=="__main__":   		
    snakeApp = Application()
    snakeApp.root.mainloop()
