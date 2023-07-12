import pygame

# Graphics
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
LIGHT_GRAY = (200,200,200)
GRAY = (100, 100, 100)
BLACK = (0,0,0)
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10
FONT_PATH = pygame.font.match_font("arial")

# Keyboard mode
MOVEMENT_KEYS = ( pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT )
SELECTION_KEYS = (pygame.K_SPACE,pygame.K_RETURN)
SELECT_MODE = pygame.USEREVENT + 1


DEBUG = False

NUM_PLAYERS = 2