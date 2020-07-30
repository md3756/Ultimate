import MamaBoard as mb
import Player as p
import pygame, math

class GameManager:
    def __init__(self):
        """
            Initialize important parameters for game playing.
        """
        self.players = []
        # Temporary default tokens
        tokens = ["./o.png", "./x.png"]
        # tokens = ['x', 'o']

        # TODO: Have this info input by players
        self.num_players = 2

        # Initialize all players with tokens
        for i in range(self.num_players):
            # TODO: Have this info input by players
            self.players.append(p.Player(tokens[i]))

        # Index of player whose turn it is
        self.turn = 0

        # TODO: Have this info input by players
        self.dimension = 3

        pygame.init()

        # Set initial values for screen and game
        # self.font = pygame.font.SysFont('Arial', 40)
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        background_color = (255,255,255)
        self.screen.fill(background_color)
        pygame.display.set_caption("Ultimate TicTacToe")
        self.clock = pygame.time.Clock()

        # Initialize and draw Mamaboard
        self.game = mb.MamaBoard(self.width, self.screen, self.dimension)
        self.game.draw_board()

        # Iterate over all rows of babyboards within mamaboard
        # note: offset_x is the row a babyboard is in (from 0 to self.dimension - 1)
        for offset_x, babylist in enumerate(self.game.board):
            # Iterate over each babyboard within the row babylist
            # note: offset_y is the column that baby is in (0 to self.dimension - 1)
            for offset_y, baby in enumerate(babylist):
                # Draw the babyboard
                baby.draw_board(offset_x, offset_y)

    def update(self):
        """
            Function to process events initiated by the player(s), place a
            token in the square clicked by the user (if valid), and update the
            turn variable to allow the next player to move.
        """
        # Identify current player based on the integer self.turn
        cur_player = self.players[self.turn]

        # Sleep to make the game 60 fps
        self.clock.tick(60)

        # Retrieve any events that have happened and iterate over all events
        for event in pygame.event.get():
            # If the event was a click event, player must be trying to make a move
            if pygame.mouse.get_pressed()[0]:
                # Get coordinates of where player clicked
                self.mouse_posn = pygame.mouse.get_pos()
                # text = self.font.render(cur_player.token, False, (128,0,128))

                # Try to make the move the player indicated
                try:
                    # Identify exact square clicked by player from mouse
                    # position
                    mama_coord, baby_coord = self.game.convert(self.mouse_posn)
                    print("mama, baby",mama_coord, baby_coord)

                    # Given a location (mama_coord and baby_coord), try to
                    # place token
                    self.game.move(mama_coord, baby_coord, cur_player)

                    # Calculate location that player's token should appear on
                    # board given mouse position
                    location = self.game.place_token(self.mouse_posn)

                    # Display the player's token on the desired location
                    self.screen.blit(cur_player.token, location)

                    # Update player to next player since move was made successfully
                    self.turn = (self.turn + 1) % self.num_players
                    break

                # If ValueError is raised, the move was placed in an invalid
                # location (spot already occupied, within the wrong babyboard,
                # etc.). Should try again
                except ValueError:
                    print("try again friend")
                # If AssertionError is raised, player did not click mouse
                # within any of the squares. Should try again
                except AssertionError:
                    print("out of range")
                    continue


            # Quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        # Update the screen
        pygame.display.flip()

    def play(self):
        """
            Function to actually play a game given an initialized GameManager.
        """
        # Play forever until player quits the game
        while True:
            # Update the board with new moves
            self.update()


gm = GameManager()
gm.play()
