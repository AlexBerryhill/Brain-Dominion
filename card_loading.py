from treasure_card import Treasure_card
from victory_card import Victory_card
from kingdom_card import Kingdom_card
import json
import random
DEBUG = True
def load_cards():
    '''Using the cards.json file, returns a list of all the cards in the dominion game as objects.'''
    cards = []
    with open('assets/cards.json') as file:
        cards_file = json.load(file)
        for card in cards_file['Dominion']:
            if card['type'] == 'Treasure':
                cards.append(Treasure_card(card['name'],card['cost'],card['worth'],card['id'],card['starting_amount']))
            elif card['type'] == 'Victory':
                cards.append(Victory_card(card['name'],card['cost'],card['victory_points'],card['id'],card['starting_amount']))
            else:
                cards.append(Kingdom_card(card['name'],card['cost'],card['description'],card['plus_actions'],card['plus_treasure'],card['plus_buys'],card['plus_cards'],card['is_attack'],card['is_reaction'],card['id'],card['special_action']))
    return cards

def setup_game_cards(cards):
    '''Pulls the cards from the card list needed for a game (all victory and treasure cards and 10 kingdom cards)
    Returns a dictionary of card id's and the amount of that card there is at the start. 
    '''
    game_cards = cards[:7]
    used_cards = [0]

    #TEMPORARY CODE FOR DEBUGGING NEW KINGDOM CARD CODE
    if DEBUG:
        game_cards.append(cards[8])
        used_cards.append(cards[8])

    for _ in range(10 if DEBUG else 11):
        card_i = 0
        while card_i in used_cards:
            # card_i = random.randint(7,31) 
            blacklist = [25,26]
            card_i = random.choice([x for x in range(7,32) if x not in blacklist])
        game_cards.append(cards[card_i])
    
    supply = {}
    for card in game_cards:
        supply[card.id] = card.starting_amount
    return supply