import random
random.seed(100)
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
    
class SpecialWildCard:
    def __init__(self,action):
        self.action = action
        self.colour =None
        self.number=None

    def __str__(self):
        return f"{self.action}"
    
    def __str__(self):
        if self.colour:
            return f"{self.colour}_{self.action}"
        else:
            return f"{self.action}"
    
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
            for i in range(4):
                wild_card = SpecialWildCard(special_wild_card)
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
#################Load Things#########
initial_pack =Deck()
initial_pack.create_deck()
print("these are shuffled")
initial_pack.shuffle()
for shuffledcards in initial_pack.pack:  ##show shuffled pack###
    print(shuffledcards) 
#####################################

class Player:
    def __init__(self, number):
        self.number = number
        self.hand = [] #needs to be a list of cards
        
        #self.turn = turn
    def __str__(self, ) -> str:
        return self.number
    

class startGame:
    def __init__(self):
        self.discard_pile = []
        self.players = [] #keep a list of players
        self.current_player_index = 0
        self.counter=0
        self.reverse=False # true is anticlockwise   
        
    def deal(self):
        num_players = int(input("Enter the number of players: "))
        self.players = [Player(f"player{i+1}") for i in range(0,num_players)]
        
##Deal to players########

        for _ in range(7):  # Loop for each card to be dealt
            for player in self.players:
                drawn_card = initial_pack.draw_card()
                if drawn_card:
                    player.hand.append(drawn_card)

            #def start_game(self):
        for player in self.players:
            player.hand=[card for card in player.hand]
            print(f"{player.number}'s hand: {[str(card) for card in player.hand]}")
    
    def discard(self):
        
        while True:
            top_card = initial_pack.draw_card()
            #self.discard_pile.append(str(top_card))
            self.discard_pile.append(top_card)
            print(f"Top card on the discard pile: {top_card}")
            ###just checking it actually went there ####
            #print(f"this is the whole discard pile:{self.discard_pile}")

            if type(top_card) == WildCard and top_card.action in ["wild", "pick_up_4"]:
                    print(f"Unsuitable start card (wild card), flip again")
            else:
                    #print(f"Top card on the discard pile is: {top_card}")
                break
            
    
       
    def play_card(self, Player):
        while True:
            current_player = self.players[self.current_player_index]
            current_player_hand = current_player.hand
            print(f"{current_player}, it is your turn, which card would you like to play from your hand: {', '.join(map(str, current_player_hand))}")
            chosen_card_index = int(input("Enter the index of the card you want to play: "))
            played_card = current_player_hand[chosen_card_index]
            discarded_card_in_play = self.discard_pile[-1]

        
            if (str(played_card) == "wild" or str(played_card) == "pick_up_4" or
                    (hasattr(played_card, 'colour') and played_card.colour == discarded_card_in_play.colour) or
                    (hasattr(played_card, 'number') and played_card.number == discarded_card_in_play.number)):
                self.discard_pile.append(played_card)
                current_player.hand.remove(played_card)  # Remove the card from the player's hand
                #self.current_player_index = (self.current_player_index + 1) % len(self.players)
                print(f"top card on the discard pile is {played_card}")
                
                
                if str(played_card) =="wild":
                    while True:
                        #ask user to choose a colour
                        wild_colour= input("Enter your chosen wild card colour? ").lower()
                        if wild_colour in["red", "yellow","green","blue"]:
                            played_card.colour=wild_colour
                            self.discard_pile.append(played_card)
                            print(f"top card on the discard pile is {played_card}")

                            break
                        else:
                            print(f"invalid colour chosen, choose again")
                            
                
                elif str(played_card) =="pick_up_4":
                    while True:
                    #ask user to choose a colour
                        four_colour= input("Enter your chosen pick_up_4 card colour? ").lower()
                        if four_colour in["red", "yellow","green","blue"]:
                            played_card.colour=four_colour
                            print(f"top card on the discard pile is {played_card}")
                            
                            break
                        else:
                            print(f"invalid colour chosen, choose again")
                
                elif "pick_up_2" in str(played_card):
                    self.counter +=2
                    print(self.counter)
                    # go to next player
                    #game1.pick_up(current_player)

                elif "miss_a_turn" in str(played_card):
                   self.current_player_index = (self.current_player_index + 1) % len(self.players)
                   print(f" Player {self.current_player_index+1} You miss a turn")

                elif "reverse" in str(played_card):
                    self.reverse= not self.reverse # using not keyword as a flip
                    
                break  # Exit the loop as the player successfully played a card
                
                
            else:
                print("Can't play that card.")
                game1.pick_up(current_player)

                # drawn_card = initial_pack.draw_card()
                # current_player.hand.append(drawn_card)
                # print(f"{current_player} has picked up {drawn_card}")
                break
        self.next_player(self.current_player_index)
##Move to the next player##
    def next_player(self, current_player_index):
        if self.reverse==False:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.play_card(self.players)
        else:
            self.current_player_index = (self.current_player_index - 1) % len(self.players)
            self.play_card(self.players)
##Pick up Cards
    def pick_up(self,current_player):
        if self.counter>=1:
            for i in range(self.counter):
                drawn_card = initial_pack.draw_card()
                current_player.hand.append(drawn_card)
                print(f"{current_player} has picked up {drawn_card}") 
                
        else:
            drawn_card = initial_pack.draw_card()
            current_player.hand.append(drawn_card)
            print(f"{current_player} has picked up {drawn_card}")


                
                

################## call things ###################
#startGame()
initial_pack.shuffle()
for shuffledcards in initial_pack.pack:  ##show shuffled pack###
    print(shuffledcards) 
game1=startGame()
game1.deal()
game1.discard()
game1.play_card(game1.players)
