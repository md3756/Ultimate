import MamaBoard as mb
import Player as p
import pygame

class GameManager:
    def __init__(self):
        # self.players = []
        # self.num_players = int(input("Input number of players: "))
        # # Initialize all players with tokens
        # for i in range(self.num_players):
        #     token = input("Input player " + str(i)+ "'s token: ")
        #     self.players.append(p.Player(token))

        # # Index of player whose turn it is
        # self.turn = 0
        #
        # self.dimension = int(input("Input number of dimensions: "))
        # self.game = mb.MamaBoard(self.dimension)

        #1
        pygame.init()
        width, height = 500, 500
        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ultimate TicTacToe")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()

    def update(self):
        # Sleep to make the game 60 fps
        self.clock.tick(60)

        # Clear the screen
        self.screen.fill(0)

        for event in pygame.event.get():
            # Quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # Update the screen
        pygame.display.flip()

    def play(self):
        print("Starting game...")
        while True:
            self.update()
            # self.game.print_mama_board()
            # cur_player = self.players[self.turn]
            # print("Player", self.turn + 1, "GO!")
            #
            # value = input("Input a move (mbx mby bbx bby): ")
            # if value == "q": break
            # mbx, mby, bbx, bby = value.split(" ")
            # self.game.move(int(mbx), int(mby), int(bbx), int(bby), cur_player)
            # self.turn = (self.turn + 1) % self.num_players

gm = GameManager()
gm.play()
