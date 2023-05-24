import pygame
import random
import io
import urllib.request
# https://www.ultraboardgames.com/dominion/gfx/<card_name>.jpg
# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 20

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dominion")

# Define Dominion card class
class DominionCard:
    def __init__(self, name, cost, type):
        self.name = name
        self.cost = cost
        self.type = type
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.image = self.load_image()

    def __str__(self):
        return self.name

    def load_image(self):
        image_url = f"https://www.ultraboardgames.com/dominion/gfx/{self.name}.jpg"
        try:
            print(f"Loading image for {self.name} at {image_url}")
            with urllib.request.urlopen(image_url) as url:
                print(f"Image loaded for {self.name}")
                image_data = url.read()
                image_stream = io.BytesIO(image_data)
                image = pygame.image.load(image_stream).convert()
                image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                return image
        except:
            print(f"Error loading image for {self.name}:", flush=True)
            # If image loading fails, create a placeholder image
            image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            image.fill(WHITE)
            pygame.draw.rect(image, BLACK, image.get_rect(), 3)
            return image

    def draw(self, surface, x, y):
        self.rect.topleft = (x, y)
        surface.blit(self.image, self.rect.topleft)



# Define Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = []
        self.discard = []

    def draw_cards(self, num_cards, supply):
        for _ in range(num_cards):
            if not self.deck:
                self.deck = self.discard
                self.discard = []
                random.shuffle(self.deck)
            if self.deck and supply:
                card = random.choice(list(supply))
                self.hand.append(card)
                supply.remove(card)

    def play_card(self, index):
        if index >= 0 and index < len(self.hand):
            return self.hand.pop(index)

    def end_turn(self):
        self.discard.extend(self.hand)
        self.hand = []

    def __str__(self):
        return self.name


# Initialize game objects
player1 = Player("Player 1")
player2 = Player("Player 2")
game = [player1, player2]
cards = [
    DominionCard("Copper", 0, "Treasure"),
    DominionCard("Silver", 3, "Treasure"),
    DominionCard("Gold", 6, "Treasure"),
    DominionCard("Estate", 2, "Victory"),
    DominionCard("Duchy", 5, "Victory"),
    DominionCard("Province", 8, "Victory"),
    # Add more cards...
]

# Set up initial player decks
for player in game:
    for _ in range(7):
        player.deck.append(cards[0])  # Copper
    for _ in range(3):
        player.deck.append(cards[4])  # Estate
    random.shuffle(player.deck)

# Set up the supply stacks
supply = {
    cards[0]: 60,  # Copper
    cards[1]: 40,  # Silver
    cards[2]: 30,  # Gold
    cards[3]: 8,   # Estate
    cards[4]: 8,   # Duchy
    cards[5]: 8    # Province
    # Add more cards...
}

# Each player draws 5 cards
for player in game:
    player.draw_cards(5, list(supply.keys()))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                # Check if the player clicked on a supply stack
                for i, card in enumerate(supply):
                    if card.rect.collidepoint(mouse_pos):
                        # Draw a card from the selected supply pile
                        if supply[card] > 0:
                            player.draw_card(card)
                            supply[card] -= 1

    # Clear the screen
    window.fill(GRAY)

    # Draw supply stacks
    supply_x = WINDOW_WIDTH - CARD_MARGIN - CARD_WIDTH
    supply_y = CARD_MARGIN
    for i, card in enumerate(supply):
        card.draw(window, supply_x, supply_y + i * (CARD_HEIGHT + CARD_MARGIN))

    # Draw player hands
    for i, player in enumerate(game):
        for j, card in enumerate(player.hand):
            card_x = CARD_MARGIN + (CARD_WIDTH + CARD_MARGIN) * j
            card_y = WINDOW_HEIGHT - CARD_MARGIN - CARD_HEIGHT - (CARD_HEIGHT + CARD_MARGIN) * i
            card.draw(window, card_x, card_y)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
