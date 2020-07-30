import pygame, math

TIE = "tie"
class BabyBoard:
    """
        Class representing one of the 9 sub-boards in the Ultimate game.
    """
    def __init__(self, buffer, draw_length, mama_buffer, screen):
        """
        Example board:
            [[?,?,?],[?,?,?],[?,?,?]]

                ? | ? | ?
                ? | ? | ?
                ? | ? | ?
        """
        # Board variable storing tokens placed on board so far. None indicates
        # an empty space
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        # Count number of moves made so far
        self.move_counter = 0
        # Store winner of this particular BabyBoard
        self.winner = None
        # Dimension of BabyBoard should always be 3, unlike MamaBoard
        self.dimension = 3
        # Store values indicating how each BabyBoard should be drawn
        self.buffer = buffer
        self.draw_length = draw_length
        self.mama_buffer = mama_buffer
        self.screen = screen

    def move(self, x, y, player):
        """
            Play a move.
            input:
                x (int): row token was placed on BabyBoard
                y (int): column token was placed on BabyBoard
                token: player's token
        """
        # If there is already a winner of this board, no moves can be made
        if self.winner: return
        # If there is already a token placed at this position, raise an error
        if self.board[x][y]:
            raise ValueError("Position " + str((x,y)) + " is taken.")

        # Otherwise, move can be made successfully, increment counter and place
        # token
        self.move_counter += 1
        self.board[x][y] = player.token

        # Check if this move placed caused a win for this BabyBoard
        if self.check_win(x, y, player):
            # If player won this board, increment their point counter
            player.points += 1
            print("WINNER:", self.winner)
        else:
            print("STILL NO WINNER, LOSER")

    def check_win(self, x, y, player):
        """
            Check if putting token in (x,y) is a winning move for this board.

            inputs:
                x (int): row token was placed on BabyBoard
                y (int): column token was placed on BabyBoard
                player (Player): player who made the move

            returns winner of BabyBoard (None for no winner, player.token for a
            win by player, and TIE for a tie)

        """
        token = player.token
        # If less than 3 moves have been made on this board, win is not
        # possible so return
        if self.move_counter < 3: return None
        # Check if all elements of row x == token
        if all(item == self.board[x][0] for item in self.board[x]):
            self.winner = token

        # Check if all elements of col y == token
        elif all(self.board[idx][y] == self.board[0][y] for idx in range(1,3)):
            self.winner = token

        # If in corner or middle, check if diagonal elements == x
        # left-to-right
        elif all(self.board[a][a] == self.board[0][0] for a in range(1, 3)):
            self.winner = token
        # right-to-left diagonal
        elif all(self.board[a][b] == self.board[2][0] for a, b in [(0,2), (1,1)]):
            self.winner = token
        # All spots have bin filled but there is no winner, indicate a tie
        elif self.move_counter >= 9:
            self.winner = TIE
        return self.winner

    def draw_board(self, offset_x, offset_y):
        """
            Function to draw a BabyBoard.

            inputs:
                offset_x (int): row of MamaBoard containing this BabyBoard
                offset_y (int): column of MamaBoard containing this BabyBoard
        """
        # Identify properties of line
        color = (255,0,0)
        line_width = math.floor(5)

        # Amount of space taken up by one full BabyBoard in both directions
        previous_x = 2*self.buffer + self.draw_length
        previous_y = 2*self.buffer + self.draw_length

        # Iterate over lines to be drawn
        for i in range(1, self.dimension):
            # Identify start and end coordinates of vertical lines to draw
            start = (previous_x*offset_x + self.buffer + self.mama_buffer + i*self.draw_length/self.dimension, previous_y*offset_y + self.buffer + self.mama_buffer)
            end = (start[0], start[1] + self.draw_length)
            pygame.draw.line(self.screen, color, start, end, line_width)

            # Identify start and end coordinates of horizontal lines to draw
            start = (previous_x*offset_x + self.buffer + self.mama_buffer, previous_y*offset_y + self.buffer + self.mama_buffer + i*self.draw_length/self.dimension)
            end = (start[0] + self.draw_length, start[1])
            pygame.draw.line(self.screen, color, start, end, line_width)

            # Update display with the lines
            pygame.display.flip()

    def print_board(self):
        """
            Print board in more readable way.
        """
        for x in self.board:
            print(x)

def random_test():
    """
        Function testing a few values.
    """
    bb = BabyBoard()
    bb.move(0,0,"o")
    bb.move(0,1,"x")
    bb.move(0,2,"o")
    bb.move(1,0,"o")
    bb.move(1,1,"x")
    bb.move(1,2,"x")
    bb.move(2,0,"x")
    bb.move(2,1,"x")
    bb.move(2,2,"x")
    bb.print_board()
