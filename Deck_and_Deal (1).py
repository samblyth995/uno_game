#!/usr/bin/env python
# coding: utf-8

# In[156]:


import random
class Card:
#######__init__ means instatiating the object as it's created

    def __init__(self,colour,number):
  #attribute /storage
        self.colour = colour
        self.number =number
        print(colour,number)
    def __str__(self):
        return f"{self.colour}_{self.number}"
    
class WildCard:
    def __init__(self, colour,action):
        self.colour = colour
        self.action = action

    def __str__(self):
        return f"{self.colour}_{self.action}"


# In[157]:


###########  CREATE THE INITAL DECK  ########################

class Deck:
    def __init__(self):
        self.pack = []

    def create_deck(self):
        colours = ["red", "blue", "green", "yellow"]
        numbers = list(range(1, 10))
        actions = ["pick_up_2","miss_a_turn", "reverse"]
        special_wild_cards = ["wild", "pick_up_4"]
########### ADD NORMAL CARDS ##############################

        for colour in colours:
            for i in range(2):
                for number in numbers:
                    new_card = Card(colour, number)
                    self.pack.append(new_card)
        
            new_card = Card(colour, 0) 
            self.pack.append(new_card)
            print(f"Deck has {len(self.pack)} cards after adding normal cards.")
              #print(self.pack)
         
########### ADD WILD CARDS ###############################

        for wild_card_type in actions:
            for colour in colours:
                for i in range(2):
                    wild_card= WildCard(colour, wild_card_type)
                    self.pack.append(wild_card)
                    print(f"Deck has {len(self.pack)} cards after adding action cards: {wild_card}")   

        for special_wild_card in special_wild_cards:
            for colour in colours:
                wild_card = WildCard(colour, special_wild_card)
                self.pack.append(wild_card)
                print(f"Deck has {len(self.pack)} cards after adding special wild cards: {wild_card}")
    ###########Shuffle########
    def shuffle(self):
        random.shuffle(self.pack)

    #######  DRAW CARD #############
    def draw_card(self):
        if not self.is_empty():
            return self.pack.pop()
        else:
            print("The deck is empty.")
            return None

    def is_empty(self):
        return len(self.pack) == 0
    


# In[158]:


initial_pack =Deck()
initial_pack.create_deck()
print("these are shuffled")
initial_pack.shuffle()
for shuffledcards in initial_pack.pack:  ##show shuffled pack###
    print(shuffledcards) 


# In[159]:


######Deal to players########
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [] #needs to be a list of cards
        #self.turn = turn
    def __str__(self, ) -> str:
        return self.name

num_players = int(input("Enter the number of players: "))
players = [Player(f"player{i+1}") for i in range(num_players)]

for _ in range(7):  # Loop for each card to be dealt
    for player in players:
        drawn_card = initial_pack.draw_card()
        if drawn_card:
            player.hand.append(drawn_card)

for player in players:
    print(f"{player.name}'s hand: {[str(card) for card in player.hand]}")


# In[ ]:




