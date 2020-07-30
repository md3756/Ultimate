import BabyBoard as bb
import math, pygame

class MamaBoard:
    def __init__(self, length, screen, dimension=3):
        self.length = length
        self.screen = screen
        self.next_move = (None, None)
        self.dimension = dimension
        self.board = []
        self.buffer = 0.1*self.length
        self.draw_length = self.length - 2*self.buffer

        self.baby_buff = self.buffer/self.dimension
        self.baby_draw_length = (self.draw_length/self.dimension) - 2*self.baby_buff
        for i in range(self.dimension):
            self.board.append([])
            for j in range(self.dimension):
                self.board[i].append(bb.BabyBoard(self.baby_buff, self.baby_draw_length, self.buffer, self.screen))

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
            else:
                raise ValueError("Position " + str((mbx,mby)) + " is invalid.")
        # Not a valid move
        else:
            raise ValueError("Position " + str((mbx,mby)) + " is invalid.")

    def draw_board(self):
        color = (0,0,0)
        line_width = math.floor(self.length/60)
        for i in range(1, self.dimension):
            # Vertical
            start = (self.buffer + i*self.draw_length/self.dimension, self.buffer)
            end = (start[0], start[1] + self.draw_length)
            pygame.draw.line(self.screen, color, start, end, line_width)

            # Horizontal
            start = (self.buffer, self.buffer + i*self.draw_length/self.dimension)
            end = (start[0] + self.draw_length, start[1])
            pygame.draw.line(self.screen, color, start, end, line_width)

        pygame.display.flip()

    def place_token(self, mouse_posn):
        """
            Adjust mouse position to be centered within a square.

        """

        mod = self.baby_draw_length/3 # 3 = self.dimension for a babyboard object

        x = mouse_posn[0] - (mouse_posn[0] % mod) # + mod/2
        y = mouse_posn[1] - (mouse_posn[1] % mod) # + mod/2

        return (x, y)

    def convert(self, mouse_posn):
        divisor = self.draw_length/self.dimension
        x = int((mouse_posn[1] - self.buffer) // divisor)
        y = int((mouse_posn[0] - self.buffer) // divisor)
        mama = [x, y]

        # Check that mama coordinates are valid
        assert 0 <= x < self.dimension
        assert 0 <= y < self.dimension

        # Convert original mouse position to standard mouse position for one baby board
        # (x and y values are between 0 and width of a baby board's allocated space)
        # x = mouse_posn[0] - mama[1]* divisor - mama[1] * 2*self.baby_buff - self.buffer - self.baby_buff
        # y = mouse_posn[1] - mama[0]* divisor - mama[0] * 2*self.baby_buff - self.buffer - self.baby_buff
        x = mouse_posn[0] - (mama[1]*divisor + self.buffer)
        y = mouse_posn[1] - (mama[0]*divisor + self.buffer)
        new_mouse_posn = (int(x), int(y))
        # print("buff:", self.buffer)
        # print("bbuff:", self.baby_buff)
        # print("dl:", self.draw_length)
        # print("old:", mouse_posn)
        # print("new:", new_mouse_posn)

        divisor = self.baby_draw_length/3
        x = int((new_mouse_posn[1] - self.baby_buff) // divisor)
        y = int((new_mouse_posn[0] - self.baby_buff) // divisor)

        # Check that baby coordinates are valid
        assert 0 <= x < self.dimension
        assert 0 <= y < self.dimension

        #did not work --ignore
        # x = int((mouse_posn[0] - self.buffer - self.baby_buff) - mama[1] * (divisor + self.baby_buff))
        # y = int((mouse_posn[1] - self.buffer - self.baby_buff) - mama[0] * (divisor + self.baby_buff))
        baby = [x, y]

        return mama, baby

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
            coords = self.coord_list()
            first_winner = self.board[coords[0][0]][coords[0][1]].winner
            if all(self.board[a][b].winner == first_winner for a, b in coords[1:]):
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
