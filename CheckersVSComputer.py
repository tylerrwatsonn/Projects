'''
Tyler Watson
Final Project
Robert Vincent, instructor
Winter 2018
'''


import tkinter, random, time
blue_score = 0
red_score = 0
class Checkers(tkinter.Tk):
    
    DELAY = 1
    
    C_WIDTH = 700  # define window width.
    C_HEIGHT = 700      # define window height
    C_ROWS = 8
    C_COLS = 8
    C_BUTTONS = 64
    C_GAP = 10
    

    def __init__(self):
        super().__init__(None)
        #Colours to use in functions
        self.RED      = 'red'
        self.DARKRED  = '#9b0000'
        self.BLUE     = 'blue'
        self.DARKBLUE = '#00009b'

        
        self.switched = []
        self.pattern = [] # stores the pattern of colors
        self.legals = [] 
        self.player_index = 0 # index of user's last successful click.
        self.score = 0        # total score.
        self.player_turn = False # True if waiting for player clicks.
        self.comp_pieces = [0,2,4,6,9,11,13,15] #list of computer piece positions
        
        # Create the canvas.
        self.canvas = tkinter.Canvas(self,
                                     width = self.C_WIDTH,
                                     height = self.C_HEIGHT,
                                     bg = 'white')
        self.circ_id = [0]*64 # array of rectangle object id
        self.colours = ['white']*64 #Start by making each space white
        
        self.canvas.pack()
        

        # Compute dimensions of the 64 circles.
        xr = (self.C_WIDTH - self.C_GAP * (self.C_COLS + 1)) // self.C_COLS
        yr = (self.C_HEIGHT - self.C_GAP * (self.C_ROWS + 1)) // self.C_ROWS

        # Create the circles.
        for i in range(self.C_BUTTONS):
            x = i % self.C_ROWS
            y = i // self.C_ROWS
            x0 = self.C_GAP * (x + 1) + xr * x
            x1 = x0 + xr
            y0 = self.C_GAP * (y + 1) + yr * y
            y1 = y0 + yr
            # Circle is created by specifying the upper corner and lower corner.
            self.circ_id[i] = self.canvas.create_oval(x0, y0, x1, y1, fill='white')
        start = 0
        end = self.C_COLS
        row = 0
        for a in range(self.C_COLS):
            for i in range(start, end, 2):
                id = self.circ_id[i]
                if id <= 16:
                    self.canvas.itemconfig(id, fill = self.DARKRED)
                    self.canvas.update()
                    self.colours[i] = self.DARKRED
                elif id > 48:
                    self.canvas.itemconfig(id, fill = self.DARKBLUE)
                    self.canvas.update()
                    self.colours[i] = self.DARKBLUE
                else:
                    self.canvas.itemconfig(id, fill = 'gray')
                    self.canvas.update()
                    self.colours[i] = 'gray'
                
            row += 1
            if row%2 == 0:
                start += self.C_COLS - 1
                end += self.C_COLS
            else:
                start += self.C_COLS + 1
                end += self.C_COLS
                
        
                
        self.score = 0
        self.title('Checkers')
        self.after(1000, self.timer) # Kick off the timer handler.
        self.canvas.bind("<Button-1>", lambda event: self.click(event))
        self.canvas.bind("<Button-3>", lambda right_event: self.right_click(right_event))
        self.canvas.pack(expand = 1)



    def click(self, event):
        '''Handles the player's turn every time they click the mouse'''
        x = event.x
        y = event.y
        self.player_index +=1
        for i in range(self.C_BUTTONS):
            x0,y0,x1,y1 = self.canvas.coords(self.circ_id[i])
            if x >= x0 and x <= x1 and y >= y0 and y <= y1:
                break
        else:                   # break did not execute.
                return
        
        if self.colours[i] == self.DARKBLUE or self.colours[i] == self.BLUE: #Handles showing legal moves (in yellow) based on the piece that has been clicked
            for j in self.legals:
                self.canvas.itemconfig(self.circ_id[j], fill = 'gray')
            self.legals = []
            for j in range(64):
                if self.legal_move([i, j]):
                    self.legals.append(j)
                    self.canvas.itemconfig(self.circ_id[j], fill = 'yellow')
                    self.canvas.update()

            

            
        if self.colours[i] == 'white':
            self.switched = []
        elif self.colours[i] != 'gray':
            self.switched = []
            self.switched.append(i)
        else:
            self.switched.append(i)

        #Handles kinging of player pieces
        if len(self.switched) == 2: 
            if self.switched[1] < 8 and self.colours[self.switched[0]] == self.DARKBLUE:
                self.colours[self.switched[0]] = self.BLUE
            elif self.switched[1] > 56 and self.colours[self.switched[0]] == self.DARKRED:
                self.colours[self.switched[0]] = self.RED

        #Handles player piece movement to alter colour list and piece index list
        if len(self.switched) == 2 and self.legal_move(self.switched):
            self.legals.remove(self.switched[1])
            self.canvas.itemconfig(self.circ_id[self.switched[0]], fill=self.colours[self.switched[1]])
            self.canvas.itemconfig(self.circ_id[self.switched[1]], fill=self.colours[self.switched[0]])
            self.colours[self.switched[0]], self.colours[self.switched[1]] = self.colours[self.switched[1]], self.colours[self.switched[0]]
            self.canvas.update()
            ind_jumped = (self.circ_id[self.switched[0]] + self.circ_id[self.switched[1]])//2 - 1 #Formula to compute the index of the space that is jumped
            col_dist = self.circ_id[self.switched[0]]%8 - self.circ_id[self.switched[1]]%8 #Compute the distance the piece has moved to handle jumping
            if abs(col_dist) == 2 or abs(col_dist) == 6: #Handles jumping
                if self.colours[ind_jumped] == self.DARKRED or self.colours[ind_jumped] == self.RED:
                    self.colours[ind_jumped] = 'gray'
                    self.canvas.itemconfig(self.circ_id[ind_jumped], fill = 'gray')
                    self.canvas.update()
                #Line below handles multiple jumping opportunities
                if self.legal_move([self.switched[1], self.switched[1] - 14]) or self.legal_move([self.switched[1], self.switched[1] - 18]) or self.legal_move([self.switched[1], self.switched[1] + 18]) or self.legal_move([self.switched[1], self.switched[1] + 14]):
                    self.switched = []
                    return
            for j in self.legals:
                self.canvas.itemconfig(self.circ_id[j], fill = 'gray')
                self.canvas.update()
            
            self.legals = []            
            self.switched = []
            self.computer_turn()
            self.game_over()

        


    def game_over(self):
        '''Checks if there are no remaining pieces of either colour'''
        if self.DARKRED not in self.colours and self.RED not in self.colours:
            self.title('You Won! Want to play again? Click Restart')
            global blue_score
            blue_score += 1
        if self.DARKBLUE not in self.colours and self.BLUE not in self.colours:
            self.title('I Won! Want to play again? Click Restart!')
            global red_score
            red_score += 1



    def above_next_to(self,piece):
        '''Return a list of colours in adjacent spaces above a piece'''
        places = []
        places.append(self.colours[piece - 7])
        places.append(self.colours[piece - 9])
        return places

    def next_to(self, piece):
        '''Return a list of colours in adjacent spaces below a piece'''
        places = []
        if piece < 55:
            places.append(self.colours[piece + 7])
            places.append(self.colours[piece + 9])
        return places

    def switch(self,ls):
        '''Handles switching indexes/colours and reconfigures board for computer moves'''
        if len(ls) == 2: #Handles king pieces
            if ls[1] < 8 and self.colours[ls[0]] == self.DARKBLUE:
                self.colours[ls[0]] = self.BLUE
            elif ls[1] > 56 and self.colours[ls[0]] == self.DARKRED:
                self.colours[ls[0]] = self.RED
        if not self.legal_move(ls):
            return False
        self.canvas.itemconfig(self.circ_id[ls[0]], fill=self.colours[ls[1]])
        self.canvas.itemconfig(self.circ_id[ls[1]], fill=self.colours[ls[0]])
        self.colours[ls[0]], self.colours[ls[1]] = self.colours[ls[1]], self.colours[ls[0]]
        self.canvas.update()
        ind_jumped = (self.circ_id[ls[0]] + self.circ_id[ls[1]])//2 - 1
        col_dist = self.circ_id[ls[0]]%8 - self.circ_id[ls[1]]%8
        if abs(col_dist) == 2 or abs(col_dist) == 6:
                # index of jumped space computed below
                if self.colours[ind_jumped] != 'gray':
                    self.colours[ind_jumped] = 'gray'
                    self.canvas.itemconfig(self.circ_id[ind_jumped], fill = 'gray')
                    self.canvas.update()
        self.timer

    def jump_down_left(self, piece):
            '''Function for computer to jump down left and continues jumping until no jumps are legal'''
            self.switch([piece, piece + 14])
            piece += 14
            while True:
                if self.legal_move([piece, piece+14]):
                    self.switch([piece, piece + 14])
                    if piece + 14 < 64:
                        piece += 14
                elif self.legal_move([piece, piece + 18]):
                    self.switch([piece, piece + 18])
                    if piece + 18 < 64:
                        piece += 18
                else:
                    break

    def jump_down_right(self,piece):
            '''Function for computer to jump down right and continues jumping until no jumps are legal'''
            self.switch([piece, piece + 18])
            piece += 18
            while True:
                if self.legal_move([piece, piece+14]):
                    self.switch([piece, piece + 14])
                    if piece + 14 < 64:
                        piece += 14
                elif self.legal_move([piece, piece + 18]):
                    self.switch([piece, piece + 18])
                    if piece + 18 < 64:
                        piece += 18
                else:
                    break

        
    def computer_turn(self):
            '''Function to handle computer's move (priority-based)'''
            self.switched = []
            self.comp_pieces = []
            i = 0
            for item in self.colours:
                if item == self.DARKRED or item == self.RED:
                    self.comp_pieces.append(i)
                i +=1

            no_jump = True

        
            for piece_ind in reversed(self.comp_pieces): #Priority 1:Checks if computer can jump
                if piece_ind < 47 and (self.next_to(piece_ind)[0] == self.DARKBLUE or self.next_to(piece_ind)[0] == self.BLUE) and self.legal_move([piece_ind, piece_ind + 14]):
                        self.jump_down_left(piece_ind)
                        return
                elif self.colours[piece_ind] == self.RED and  (self.above_next_to(piece_ind)[0] == self.DARKBLUE or self.above_next_to(piece_ind)[0] == self.BLUE) and self.legal_move([piece_ind, piece_ind - 14]):
                    
                    self.switch([piece_ind, piece_ind - 14])
                    no_jump = False
                    return

                if piece_ind < 47 and (self.next_to(piece_ind)[1] == self.DARKBLUE or self.next_to(piece_ind)[1] == self.BLUE) and self.legal_move([piece_ind, piece_ind + 18]):
        
                        self.jump_down_right(piece_ind)
                        no_jump = False
                        return
                elif self.colours[piece_ind] == self.RED and (self.above_next_to(piece_ind)[1] == self.DARKBLUE or self.above_next_to(piece_ind)[1] == self.BLUE) and self.legal_move([piece_ind, piece_ind - 18]):
                        self.switch([piece_ind, piece_ind - 18])
                        no_jump = False
                        return

        
            for piece_ind in reversed(self.comp_pieces): #Priority 2: Simply developing a piece towards becoming a king and avoids moving into vulnerable position
                if self.colours[piece_ind] == self.DARKRED and piece_ind < 55 and self.next_to(piece_ind)[0] == 'gray':
                        self.switched.append(piece_ind)
                        self.switched.append(piece_ind+7)
                        if self.switched[1] > 56: #Prioritize getting a king
                            self.switch(self.switched)
                            return
                        if len(self.colours) > self.switched[1] + 7:
                            if self.next_to(self.switched[1])[0] != self.DARKBLUE and self.next_to(self.switched[1])[1] != self.DARKBLUE:
                                self.switch(self.switched)
                                return
                            self.switched = []
                if self.colours[piece_ind] == self.DARKRED and piece_ind < 55 and self.next_to(piece_ind)[1] == 'gray':
                        self.switched.append(piece_ind)
                        self.switched.append(piece_ind+9)
                        if self.switched[1] > 56: #Prioritize getting a king
                            self.switch(self.switched)
                            return
                        if len(self.colours) > self.switched[1] + 9:
                            if self.next_to(self.switched[1])[0] != self.DARKBLUE and self.next_to(self.switched[1])[1] != self.DARKBLUE:
                                self.switch(self.switched)
                                return

            self.comp_random() #See function below



    def comp_random(self):
        '''Function to move computer piece when no prioritized moves can be made (jump or avoiding vulnerable position)'''
        while True:
                x = random.randint(0, len(self.comp_pieces) - 1)
                a = random.choice([-7,-9,7,9])
                piece_ind = self.comp_pieces[x]
                if self.legal_move([piece_ind, piece_ind + a]):
                    self.switch([piece_ind, piece_ind + a])
                    return
            
            
            
        
    def timer(self):
        if not self.player_turn:
            self.pattern.append(random.choice(range(self.C_BUTTONS)))
            for p in self.pattern:
                break
            self.player_turn = True
    
        self.after(self.DELAY, self.timer)

    def legal_move(self,ls):
        '''Takes a list of the two spaces and determines legality of the move based on colour'''

        if ls[1]>63:
            return False
        col_dist = self.circ_id[ls[0]]%8 - self.circ_id[ls[1]]%8
        ind_jumped = (self.circ_id[ls[0]] + self.circ_id[ls[1]])//2 - 1
        
        if self.colours[ls[1]] != 'gray':
            return False

        if self.colours[ls[0]] == self.DARKBLUE: #Regular blue
            if ls[1] == (ls[0] - 9) or ls[1] == (ls[0] - 7):
                return True
            elif (abs(col_dist) == 2 or abs(col_dist) == 6) and (abs(ls[1] - ls[0]) in [14,18]):
                if self.colours[ind_jumped] == self.RED or self.colours[ind_jumped] == self.DARKRED:
                    if ls[1] < ls[0] and not(ls[0]%8 == 6 and ls[1]%8 == 0):
                        return True


        elif self.colours[ls[0]] == self.BLUE: #Blue King 
            if (ls[1] == (ls[0] + 9) or ls[1] == (ls[0] + 7)) or (ls[1] == (ls[0] - 9) or ls[1] == (ls[0] - 7)):
                return True
            elif (abs(col_dist) == 2 or abs(col_dist) == 6) and (abs(ls[1] - ls[0]) in [14,18]):
                if self.colours[ind_jumped] == self.RED or self.colours[ind_jumped] == self.DARKRED:
                    return True
            else:
                return False
            
               
        elif self.colours[ls[0]] == self.DARKRED: #Regular red
            if ls[1] == (ls[0] + 9) or ls[1] == (ls[0] + 7):
                return True
            elif abs(col_dist) == 2 or abs(col_dist) == 6:
                if self.colours[ind_jumped] == self.BLUE or self.colours[ind_jumped] == self.DARKBLUE:
                    if ls[1] > ls[0] and not(ls[0]%8 == 6 and ls[1]%8 == 0):
                        return True
            else:
                return False
        else: #Red King
            if (ls[1] == (ls[0] + 9) or ls[1] == (ls[0] + 7)) or (ls[1] == (ls[0] - 9) or ls[1] == (ls[0] - 7)):
                return True
            elif abs(col_dist) == 2 or abs(col_dist) == 6:
                if self.colours[ind_jumped] == self.BLUE or self.colours[ind_jumped] == self.DARKBLUE:
                        return True
            else:
                return False
                
    def restart_program(self): #Function that occurs when "Restart" button is clicked
        '''Resets board'''
        global blue_score
        global red_score
        app = Checkers()
        Label(app, text="Welcome to Checkers!").pack()
        Label(app, text = "Blue Score:" + str(blue_score)).pack()
        Label(app, text = "Red Score:" + str(red_score)).pack()
        Button(app, text="Restart", command=app.restart_program).pack()
        app.mainloop()

from tkinter import Tk, Label, Button

app = Checkers()
Label(app, text="Welcome to Checkers!").pack()
Label(app, text = "Blue Score:" + str(blue_score)).pack()
Label(app, text = "Red Score:" + str(red_score)).pack()
Button(app, text="Restart", command=app.restart_program).pack()
app.mainloop()

