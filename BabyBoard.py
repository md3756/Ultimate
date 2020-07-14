TIE = "tie"
class BabyBoard:
    """
        Class representing one of the 9 sub-boards in the Ultimate game.
    """
    def __init__(self):
        """
        Example board:
            [[?,?,?],[?,?,?],[?,?,?]]

                ? | ? | ?
                ? | ? | ?
                ? | ? | ?
        """
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.move_counter = 0
        self.winner = None

    def check_win(self, x, y, player):
        """
            Check if putting token in (x,y) is a winning move for this board.
        """
        token = player.token
        if self.move_counter < 3: return None
        # Check if all elements of row x == token
        if all(item == self.board[x][0] for item in self.board[x]):
            self.winner = token

        # Check if all elements of col y == token
        elif all(self.board[idx][y] == self.board[0][y] for idx in range(1,3)):
            self.winner = token

        # If in corner or middle, check if diagonal elements == x
        elif all(self.board[a][a] == self.board[0][0] for a in range(1, 3)):
            self.winner = token
        elif all(self.board[a][b] == self.board[2][0] for a, b in [(0,2), (1,1)]):
            self.winner = token
        elif self.move_counter >= 9:
            self.winner = TIE
        return self.winner

    def move(self, x, y, player):
        """
            Play a move.
            input:
                x: x-coordinate of move
                y: y-coordinate of move
                token: "x" or "o" --> player's token
        """
        if self.winner: return
        if self.board[x][y]:
            raise ValueError("Position " + str((x,y)) + " is taken.")

        self.move_counter += 1
        self.board[x][y] = player.token

        if self.check_win(x, y, player):
            player.points += 1
            print("WINNER:", self.winner)
        else:
            print("STILL NO WINNER, LOSER")

    def print_board(self):
        """
            Print board in more readable way.
        """
        for x in self.board:
            print(x)

def random_test():
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

# random_test()
