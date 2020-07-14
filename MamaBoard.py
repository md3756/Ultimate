import BabyBoard as bb

class MamaBoard:
    def __init__(self):
        self.next_move = (None, None)
        self.board = []
        for i in range(3):
            self.board.append([])
            for j in range(3):
                self.board[i].append(bb.BabyBoard())

    def move(self, bbx, bby, mbx, mby, token):
        # Either freebie or valid location on board
        if self.next_move == (None, None) or self.next_move == (mbx, mby):
            # BabyBoard has free spaces
            if self.board[mbx][mby].winner == None:
                # Try to make the move
                self.board[mbx][mby].move(bbx, bby, token)
                # Next move is freebie, babyboard has been won/tied
                if self.board[bbx][bby].winner != None:
                    self.next_move = (None, None)
                # Otherwise, next move corresponds to current move
                else:
                    self.next_move = (bbx, bby)
        # Not a valid move
        else:
            raise ValueError("Position " + str((mbx,mby)) + " is invalid.")


    def print_mama_board(self):
        counter = 0
        # self.board = [[baby,baby,baby],[etc,],[]]
        # babylist = [baby, baby, baby]
        for babylist in self.board:
            # for each baby, print the first element of its board ([move,move,move])
            # repeat with the second and third elements
            for i in range(3):
                for baby in babylist:
                    print(baby.board[i], end=" | ")
                print("AAAAHHHHHHH")
            break
# baby.board = [[move, move, move], [move, move, move], [move, move, move]]
# mama.board = [[baby, baby, baby], [baby, baby, baby], [baby, baby, baby]]
#
# baby | baby| baby
# _________________
# baby | baby| baby
# _________________
# baby | baby| baby
#
# move move move | move move move | move move move
# move move move | move move move | move move move
# move move move | move move move | move move move
# ------------------------------------------------
# etc.


mb = MamaBoard()
print(mb.print_mama_board())
