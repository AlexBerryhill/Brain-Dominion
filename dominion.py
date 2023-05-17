
import pygame
# https://www.ultraboardgames.com/dominion/gfx/<card_name>.jpg

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.window = pygame.display.set_mode((800, 800))
        self.background = pygame.image.load("./assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (800, 800))
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (i * 100, j * 100, 100, 100))
                elif self.board[i][j] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), (i * 100, j * 100, 100, 100))
                elif self.board[i][j] == 3:
                    pygame.draw.rect(screen, (0, 0, 255), (i * 100, j * 100, 100, 100))
        pygame.display.update()

class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    board = Board(8, 8)
    board.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()