import json
cards = {}
with open('assets/cards.json') as file:
    cards = json.load(file)
    for i,card in enumerate(cards['Dominion']):
       card['special_action'] = True 

with open('assets/cards.json','w') as file:
    json.dump(cards,file)
