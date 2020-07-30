import BabyBoard as bb
import math, pygame

class MamaBoard:
    def __init__(self, length, screen, dimension=3):
        """
            Initialize MamaBoard type with important values.
        """
        # Dimensions of the mamaboard
        self.length = length
        self.screen = screen
        self.dimension = dimension
        # Size of space between edge of screen and start of board lines
        self.buffer = 0.1*self.length
        # Proportionately smaller buffer -- size of space between edge of
        # MamaBoard lines and start of BabyBoard
        self.baby_buff = self.buffer/self.dimension
        # Length of actual lines to be drawn
        self.draw_length = self.length - 2*self.buffer
        # Length of lines that will make up each BabyBoard
        self.baby_draw_length = (self.draw_length/self.dimension) - 2*self.baby_buff

        # Pair representing BabyBoard the player is allowed to make a move in
        # next (based on previous moves). Note: (None, None) indicates that
        # all BabyBoards are valid
        self.next_move = (None, None)

        # Variable to hold all BabyBoard objects
        self.board = []
        # Iterate and create new BabyBoard objects to be stored in the board
        for i in range(self.dimension):
            self.board.append([])
            for j in range(self.dimension):
                self.board[i].append(bb.BabyBoard(self.baby_buff, self.baby_draw_length, self.buffer, self.screen))

    def move(self, mama_coord, baby_coord, player):
        """
            Check if attempted move is valid given the state of the board. If
            valid, proceed with the move and check if the move triggers a win
            of a BabyBoard or of the game as a whole. If invalid, raises an
            exception.

            inputs:
                mama_coord (pair of ints): pair identifying which BabyBoard the
                    attempted move was made in.
                baby_coord (pair of ints): pair identifying the spot in the
                BabyBoard in which the attempted move was made.
                player (Player): the player who made attempted the move.
        """
        # Extract x and y values
        mbx, mby = mama_coord
        bbx, bby = baby_coord
        # If attempted move is in a valid BabyBoard (the one indicated by the
        # coordinates of next_move), proceed
        if self.next_move == (None, None) or self.next_move == (mbx, mby):
            # Check if BabyBoard has free spaces, not yet been won
            if self.board[mbx][mby].winner == None:
                # Try to make the move within the BabyBoard
                self.board[mbx][mby].move(bbx, bby, player)

                # Once move has been made successfully, check if the move led
                # to player winning the BabyBoard
                if self.board[mbx][mby].winner:
                    # Check if new BabyBoard win indicates an overall game win
                    # for player
                    if self.check_win(mbx, mby, player):
                        print("DONE.")
                        return

                # Calculate valid BabyBoard for the next move
                # Corresponding BabyBoard based on current move has already
                # been won/tied (no more free spaces)
                if self.board[bbx][bby].winner != None:
                    # Next move is a freebie
                    self.next_move = (None, None)
                # Still room in corresponding board
                else:
                    self.next_move = (bbx, bby)
            else:
                raise ValueError("Position " + str((mbx,mby)) + " is invalid.")
        # Not a valid move
        else:
            raise ValueError("Position " + str((mbx,mby)) + " is invalid.")

    def draw_board(self):
        """
            Draw a MamaBoard based on dimensions and screen parameters.
        """
        # Identify parameters for lines to draw
        color = (0,0,0)
        line_width = math.floor(self.length/60)

        # Iterate over lines to be drawn
        for i in range(1, self.dimension):
            # Identify start and end coordinates of vertical lines to draw
            start = (self.buffer + i*self.draw_length/self.dimension, self.buffer)
            end = (start[0], start[1] + self.draw_length)
            pygame.draw.line(self.screen, color, start, end, line_width)

            # Identify start and end coordinates of horizontal lines to draw
            start = (self.buffer, self.buffer + i*self.draw_length/self.dimension)
            end = (start[0] + self.draw_length, start[1])
            pygame.draw.line(self.screen, color, start, end, line_width)

        # Update display with the lines
        pygame.display.flip()

    def place_token(self, mouse_posn):
        """
            Adjust mouse position to be centered within a square.

            inputs:
                mouse_posn (pair of ints): location player clicked

            returns pair of ints indicating where token should be placed.
        """

        # Length and width of one single square within a BabyBoard
        mod = self.baby_draw_length/3 # 3 = self.dimension for a BabyBoard object

        # Adjust the x and y positions of mouse-posn
        x = mouse_posn[0] - (mouse_posn[0] % mod) # + mod/2
        y = mouse_posn[1] - (mouse_posn[1] % mod) # + mod/2

        # Return updated location
        return (x, y)

    def convert(self, mouse_posn):
        """
            Function to convert coordinates on screen to a particular location
            in the tic tac toe game as understood by the MamaBoard and
            BabyBoard classes.

                inputs:
                    mouse_posn (pair of ints): location mouse was clicked on
                        screen

                returns two pairs, one indicating the BabyBoard containing the
                click and one indicating the square within that BabyBoard
                containing the click.
        """
        # Calculate the position within the MamaBoard in which the mouse was
        # clicked
        divisor = self.draw_length/self.dimension
        x = int((mouse_posn[1] - self.buffer) // divisor)
        y = int((mouse_posn[0] - self.buffer) // divisor)
        mama = [x, y]

        # Check that mama coordinates are valid
        assert 0 <= x < self.dimension
        assert 0 <= y < self.dimension

        # Convert original mouse position to standard mouse position for one baby board
        # (x and y values are between 0 and width of a baby board's allocated space)
        x = mouse_posn[0] - (mama[1]*divisor + self.buffer)
        y = mouse_posn[1] - (mama[0]*divisor + self.buffer)
        new_mouse_posn = (int(x), int(y))

        # Calculate the position within the BabyBoard in which the mouse was
        # clicked
        divisor = self.baby_draw_length/3
        x = int((new_mouse_posn[1] - self.baby_buff) // divisor)
        y = int((new_mouse_posn[0] - self.baby_buff) // divisor)
        baby = [x, y]

        # Check that baby coordinates are valid
        assert 0 <= x < self.dimension
        assert 0 <= y < self.dimension

        # Return the mama and baby coordinates
        return mama, baby

    def print_mama_board(self):
        """
            Function to print out board in helpful way (testing purposes only).
        """
        counter = 0
        # self.board = [[baby,baby,baby],[etc,],[]]
        # babylist = [baby, baby, baby]
        for babylist in self.board:
            # for each baby, print the first element of its board ([move,move,move])
            # repeat with the second and third elements
            for i in range(3):
                for baby in babylist:
                    print_list = ["." if not x else x for x in baby.board[i]]
                    print(" ".join(print_list), end=" | ")
                print()
            print("-"*int(23*self.dimension/3))

    def check_win(self, mbx, mby, player):
        """
            Check if putting token in (x,y) is a winning move for this board.
        """
        # Check if all elements of row x == token
        if all(item.winner == self.board[mbx][0].winner for item in self.board[mbx]):
            print("WINNER:", player.token)
        # Check if all elements of col y == token
        elif all(self.board[idx][mby].winner == self.board[0][mby].winner for idx in range(1,self.dimension)):
            print("WINNER:", player.token)
        # If in corner or middle, check if diagonal elements == x (diagonal
        # left-to-right)
        elif all(self.board[a][a].winner == self.board[0][0].winner for a in range(1, self.dimension)):
            print("WINNER:", player.token)
        # Check if diagonal right-to-left
        else:
            coords = self.coord_list()
            first_winner = self.board[coords[0][0]][coords[0][1]].winner
            if all(self.board[a][b].winner == first_winner for a, b in coords[1:]):
                print("WINNER:", player.token)
            # None of the possible wins were found, no winner for game yet
            else:
                print("NO WINNER")
                return False

        return True

    def coord_list(self):
        """
            Helper function to compile list of coordinates along the
            right-to-left diagonal.

            Returns list of coordinates of BabyBoards within a MamaBoard along
            the right-to-left diagonal.
        """
        l = []
        counter = self.dimension - 1
        for i in range(self.dimension):
            l.append((counter, i))
            counter -= 1
        return l
