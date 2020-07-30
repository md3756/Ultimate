import MamaBoard as mb
import Player as p
import pygame, math

class GameManager:
    def __init__(self):
        self.players = []
        # tokens = ['x', 'o']


        tokens = ["./o.png", "./x.png"]

        self.num_players = 2 #int(input("Input number of players: ")) FIX THISSSSSSSSSSSSSSSSSS
        # Initialize all players with tokens
        for i in range(self.num_players):
            #input("Input player " + str(i)+ "'s token: ") FIX THISSSSSSSSSSSSSSSSSS
            self.players.append(p.Player(tokens[i]))

        # Index of player whose turn it is
        self.turn = 0

        self.dimension = 3 #int(input("Input number of dimensions: ")) FIX THISSSSSSSSSSSSSSSSSS

        pygame.init()
        # self.font = pygame.font.SysFont('Arial', 40)
        self.width, self.height = 600, 600
        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255,255,255))
        pygame.display.set_caption("Ultimate TicTacToe")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()

        # Draw Mamaboard
        self.game = mb.MamaBoard(self.width, self.screen, self.dimension)
        self.game.draw_board()

        # Iterate over all babyboards within mamaboard and assign dimensions
        for offset_x, babylist in enumerate(self.game.board):
            for offset_y, baby in enumerate(babylist):
                baby.draw_board(offset_x, offset_y)

    def update(self, cur_player):
        # Sleep to make the game 60 fps
        self.clock.tick(60)
        row_height = self.game.length/self.dimension

        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                #
                self.mouse_posn = pygame.mouse.get_pos()
                # text = self.font.render(cur_player.token, False, (128,0,128))

                try:
                    # Convert mouse coordinate to equivalent mama board square
                    mama_coord, baby_coord = self.game.convert(self.mouse_posn)
                    print("mama, baby",mama_coord, baby_coord)

                    # Given a location (mama_coord and baby_coord), try to place token
                    self.game.move(mama_coord[0], mama_coord[1], baby_coord[0], baby_coord[1], cur_player)

                    location = self.game.place_token(self.mouse_posn)

                    self.screen.blit(cur_player.token, location)
                    # Update player to next player since move was made successfully
                    self.turn = (self.turn + 1) % self.num_players
                    break
                except ValueError:
                    # Placing token threw exception, move was invalid
                    print("try again friend")
                except AssertionError:
                    print("out of range")
                    continue


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
