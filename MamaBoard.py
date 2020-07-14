import BabyBoard as bb
# import Player as player

class MamaBoard:
    def __init__(self, dimension=3):
        self.next_move = (None, None)
        self.dimension = dimension
        self.board = []
        for i in range(self.dimension):
            self.board.append([])
            for j in range(self.dimension):
                self.board[i].append(bb.BabyBoard())

    def move(self, mbx, mby, bbx, bby, player):
        # Either freebie or valid location on board
        if self.next_move == (None, None) or self.next_move == (mbx, mby):
            # BabyBoard has free spaces
            if self.board[mbx][mby].winner == None:
                # Try to make the move
                self.board[mbx][mby].move(bbx, bby, player)
                if self.board[mbx][mby].winner:
                    if self.check_win(mbx, mby, player):
                        print("DONE.")
                        return
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
                    print_list = ["." if not x else x for x in baby.board[i]]
                    print(" ".join(print_list), end=" | ")
                print()
            print("-"*int(23*self.dimension/3))

    def check_win(self, mbx, mby, player):
        """
            Check if putting token in (x,y) is a winning move for this board.
        """
        # if self.move_counter < 3: return None
        # Check if all elements of row x == token
        if all(item.winner == self.board[mbx][0].winner for item in self.board[mbx]):
            print("WINNER:", player.token)
        # Check if all elements of col y == token
        elif all(self.board[idx][mby].winner == self.board[0][mby].winner for idx in range(1,self.dimension)):
            print("WINNER:", player.token)
        # If in corner or middle, check if diagonal elements == x
        elif all(self.board[a][a].winner == self.board[0][0].winner for a in range(1, self.dimension)):
            print("WINNER:", player.token)
        else:
            coords = self.coord_list
            if all(self.board[a][b].winner == coords[0].winner for a, b in coords[1:]):
                print("WINNER:", player.token)
            else:
                print("NO WINNER")
                return False
        return True

    def coord_list(self):
        l = []
        counter = self.dimension - 1
        for i in range(self.dimension):
            l.append((counter, i))
            counter -= 1
        return l


# mb = MamaBoard(5)
# mb.print_mama_board()
# exit(0)
# while True:
#     value = input("Input a move (mbx mby bbx bby token): ")
#     if value == "q": break
#     mbx, mby, bbx, bby, token = value.split(" ")
#     mb.move(int(mbx), int(mby), int(bbx), int(bby), token)
#     mb.print_mama_board()