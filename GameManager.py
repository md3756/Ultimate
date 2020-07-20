import MamaBoard as mb
import Player as p
import pygame, math

class GameManager:
    def __init__(self):
        self.players = []
        tokens = ['x', 'o']
        self.num_players = 2 #int(input("Input number of players: "))
        # Initialize all players with tokens
        for i in range(self.num_players):
            token = tokens[i] #input("Input player " + str(i)+ "'s token: ")
            self.players.append(p.Player(token))

        # Index of player whose turn it is
        self.turn = 0

        self.dimension = 3 #int(input("Input number of dimensions: "))
        self.game = mb.MamaBoard(self.dimension)

        pygame.init()
        self.font = pygame.font.SysFont('Arial', 20)
        self.width, self.height = 600, 600

        # Mamaboard dimensions are equal to screen dimensions
        self.game.length = self.width
        self.baby_length = math.floor(self.game.length / self.dimension)

        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255,255,255))
        pygame.display.set_caption("Ultimate TicTacToe")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()

        # Draw Mamaboard
        self.draw_board(self.game)

        # Iterate over all babyboards within mamaboard and assign dimensions
        for offset_w, babylist in enumerate(self.game.board):
            for offset_h, baby in enumerate(babylist):
                baby.length = self.baby_length
                self.draw_board(baby, offset_w, offset_h)
            #     break
            # break




    def draw_board(self, board_obj, offset_w=0, offset_h=0):
        self.sub = math.floor(self.baby_length/10)
        if board_obj.length == self.width:
            color = (0,0,0)
            add_w, add_h = self.sub, self.sub
        else:
            # HERE ARE OUR PROBLEMS:
            # SHE'S MIGRATING: TOP ROW OF BOARDS ARE TOO CLOSE TO THE TOP/LEFT,
            # BOTTOM ROW OF BOARDS ARE TOO CLOSE TO THE BOTTOM/RIGHT. ONLY BABY
            # BOARD THAT WORKS IS THE CENTER BOARD. NEED TO MULTIPLY SELF.SUB
            # BELOW BY SOME VALUE TO GET ALL BOARDS TO BE CENTERED WITHIN THE
            # PROVIDED SPACE
            # MAYBE: DO SOME EXAMPLES, FIGURE OUT EXACT LOCATION OF START AND
            # END POSITIONS FOR A FEW BOARDS AND CALCULATE SELF.SUB SHOULD BE
            # AND SEE WHAT THE RELATIONSHIP IS.
            add_w = self.sub*(0.5 + 1/(offset_w + 1)) + (board_obj.length)*(offset_w)
            add_h = self.sub*(0.5 + 1/(offset_h + 1)) + (board_obj.length)*(offset_h)
            print(offset_w, offset_h)
            color = (255,0,0)

        line_width = math.floor(self.width/60)
        self.draw_length =  board_obj.length - 2*self.sub
        # Drawing a board
        for i in range (1, board_obj.dimension):
            print(i, board_obj.dimension)

            # Horizontal
            # + offset_w*self.draw_length, + offset_h*self.draw_length
            start_pos = (add_w , add_h + self.draw_length*(i/board_obj.dimension))
            end_pos = (start_pos[0] + self.draw_length, start_pos[1])
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)

            # Vertical
            start_pos = (add_w + self.draw_length*(i/board_obj.dimension), add_h)
            end_pos = (start_pos[0], start_pos[1] + self.draw_length)
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)
            print(start_pos, end_pos)



        pygame.display.flip()


    def convert(self, mouse_posn, divisor):
        return [mouse_posn[1] // divisor, mouse_posn[0] // divisor]

    def place_token(self, mama_coord, baby_coord):
        # [0, 1] [1, 1] --> full_board: 900 perf_mouse_posn: [450, 150]
        # [0, 1] [1, 2] --> [550, 150]
        # [1, 1] [0, 1] --> [450, 350]
        third = self.baby_length/ 3
        x = mama_coord[1]*self.baby_length + baby_coord[1]*third + third/ 2 - self.sub/3
        y = mama_coord[0]*self.baby_length + baby_coord[0]*third + third/ 2 - self.sub/3
        print(x, y)

        return (x,y)

    def update(self, cur_player):
        # Sleep to make the game 60 fps
        self.clock.tick(60)

        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                #
                mouse_posn = pygame.mouse.get_pos()
                print(mouse_posn)
                text = self.font.render(cur_player.token, False, (128,0,128))
                # Convert mouse coordinate to equivalent mama board square
                mama_coord = self.convert(mouse_posn, self.baby_length)

                # Get new mouse position within baby board
                x = mouse_posn[0] - mama_coord[1]*self.baby_length
                y = mouse_posn[1] - mama_coord[0]*self.baby_length
                new_mouse_posn = (x, y)
                # Convert mouse position to identify location in baby board
                baby_coord = self.convert(new_mouse_posn, math.floor(self.baby_length / 3))

                try:
                    # Given a location (mama_coord and baby_coord), try to place token
                    self.game.move(mama_coord[0], mama_coord[1], baby_coord[0], baby_coord[1], cur_player)

                    location = self.place_token(mama_coord, baby_coord)

                    # location = mouse_posn # self.place_token(mama_coord, baby_coord)

                    self.screen.blit(text, location)
                    # Update player to next player since move was made successfully
                    self.turn = (self.turn + 1) % self.num_players
                    break
                except ValueError:
                    # Placing token threw exception, move was invalid
                    print("try again friend")


            # Quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # Update the screen
        pygame.display.flip()

    def play(self):
        while True:
            self.update(self.players[self.turn])


gm = GameManager()
gm.play()
