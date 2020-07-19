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
        self.width, self.height = 300, 300

        # Mamaboard dimensions are equal to screen dimensions
        self.game.length = self.width
        self.baby_length = math.floor(self.game.length / self.dimension)

        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
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


    def draw_board(self, board_obj, offset_w=0, offset_h=0):
        color = (255,255,255)
        sub = math.floor(self.baby_length/10)
        line_width = math.floor(self.width/60)
        # Drawing a board
        for i in range (1, self.dimension):
            # # Horizontal
            start_pos = (sub + offset_w*board_obj.length, offset_h*board_obj.length + board_obj.length*(i/self.dimension))
            end_pos = (start_pos[0] + board_obj.length - 2*sub , start_pos[1])
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)

            # Vertical
            start_pos = (offset_w*board_obj.length + board_obj.length*(i/self.dimension), sub + offset_h*board_obj.length)
            end_pos = (start_pos[0], start_pos[1] + board_obj.length - 2*sub)
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)

        pygame.display.flip()


    def convert(self, mouse_posn, divisor):
        return [mouse_posn[1] // divisor, mouse_posn[0] // divisor]

    def update(self, cur_player):
        # Sleep to make the game 60 fps
        self.clock.tick(60)

        player = 0
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                mouse_posn = pygame.mouse.get_pos()
                text = self.font.render(cur_player.token, False, (128,0,128))
                mama_coord = self.convert(mouse_posn, self.baby_length)
                x = mouse_posn[0] - mama_coord[1]*self.baby_length
                y = mouse_posn[1] - mama_coord[0]*self.baby_length
                new_mouse_posn = (x, y)
                baby_coord = self.convert(new_mouse_posn, math.floor(self.baby_length / 3))

                try:
                    self.game.move(mama_coord[0], mama_coord[1], baby_coord[0], baby_coord[1], cur_player)
                    self.screen.blit(text, mouse_posn)
                    break
                except ValueError:
                    print("try again friend")


            # Quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # Update the screen
        pygame.display.flip()

    def play(self):
        # print("Starting game...")
        while True:
            self.update(self.players[self.turn])
            self.turn = (self.turn + 1) % self.num_players

gm = GameManager()
gm.play()
