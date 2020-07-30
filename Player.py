import pygame


class Player:
    def __init__(self, token="x.png"):
        self.set_token(token)
        self.points = 0
        self.my_turn = False
        self.name = None

    def set_token(self, img):
        token = pygame.image.load(img)
        token = pygame.transform.scale(token, (40,40))
        self.token = token

        print("size",token.get_width(), token.get_height())
