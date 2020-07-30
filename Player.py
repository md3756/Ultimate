import pygame

class Player:
    def __init__(self, token="x.png"):
        """
            Initialization of player's attributes.
        """
        # Set the token to the input
        self.set_token(token)
        # Counter for player's point total
        self.points = 0
        # Indicate whether or not it's a player's turn
        self.my_turn = False
        # Variable storing player's name
        self.name = None

    def set_token(self, img):
        """
            Function to set a player's token to an image loaded from an input
            path.

            inputs:
                img (str): path to .png file to be used as a player's token

        """
        size = (40,40)
        # Load the image
        token = pygame.image.load(img)
        # Transform it to be the right size
        token = pygame.transform.scale(token, size)
        # Set the player object's token to the image
        self.token = token
