# import json
# cards = {}
# with open('assets/cards.json') as file:
#     cards = json.load(file)
#     for i,card in enumerate(cards['Dominion']):
#        card['special_action'] = True 

# with open('assets/cards.json','w') as file:
#     json.dump(cards,file)

my_list = [5,3,2,10]
my_list.pop(1)
print(my_list)