
import random
import numpy as np

random.seed(8)
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
        self.number = None

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
            #print(f"Deck has {len(self.pack)} cards after adding normal cards.")
              #print(self.pack)
         
########### ADD WILD CARDS ###############################

        for wild_card_type in actions:
            for colour in colours:
                for i in range(2):
                    wild_card= WildCard(colour, wild_card_type)
                    self.pack.append(wild_card)
                    #print(f"Deck has {len(self.pack)} cards after adding action cards: {wild_card}")   

        for special_wild_card in special_wild_cards:
            for i in range(4):
                wild_card = SpecialWildCard(special_wild_card)
                self.pack.append(wild_card)
                #print(f"Deck has {len(self.pack)} cards after adding special wild cards: {wild_card}")
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
        self.game_counter = 0
        self.reverse=False # true is anticlockwise   

    # track the number of games
    def start_new_game(self):
        self.game_counter += 1 
        print(f"Starting Game #{self.game_counter}")    
        
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

            if type(top_card) == WildCard and top_card.action in [ "pick_up_2","miss_a_turn", "reverse"] or type(top_card)== SpecialWildCard:
                    print(f"Unsuitable start card (wild card), flip again")

            else:
                    #print(f"Top card on the discard pile is: {top_card}")
                break
            
    
       
    def play_card(self, Player):
        while True:
            current_player = self.players[self.current_player_index]
            current_player_hand = current_player.hand

            print(f"{current_player}, it is your turn, which card would you like to play from your hand: {', '.join(map(str, current_player_hand))}")
            
            
            chosen_card_index = input("Enter the index of the card you want to play or enter 'P' to pick up: ")
            #drop to pick up card
            if chosen_card_index.upper() == 'P':
                self.pick_up(current_player)
                break

            
            #convert str to int
            chosen_card_index=int(chosen_card_index)
            #check index is in range
            
            if chosen_card_index not in range(len(current_player_hand)):
                    print("you have not chosen a valid card index.")
                    game1.play_card(current_player)
                    break

            played_card = current_player_hand[chosen_card_index]
            discarded_card_in_play = self.discard_pile[-1]
            

    
            if (str(played_card) == "wild" or str(played_card) == "pick_up_4" or
                    (hasattr(played_card, 'colour') and played_card.colour == discarded_card_in_play.colour) or
                    (hasattr(played_card, 'number') and played_card.number == discarded_card_in_play.number)):
                self.discard_pile.append(played_card)
                current_player.hand.remove(played_card)  # Remove the card from the player's hand
                #self.current_player_index = (self.current_player_index + 1) % len(self.players)
                print(f"top card on the discard pile is {played_card}")
                
                self.check_played_card(played_card, current_player,self.current_player_index)
                #Declare a winner
                if not current_player.hand:
                            print(f"Player {current_player} has won the game by playing their last card!")
                            return "Game Over"
                break  # Exit the loop as the player successfully played a card
                
               
            else:
                print("Can't play that card,if you dont have a card to play press P to pick up")
                game1.play_card(current_player)
            break
                
        self.next_player(self.current_player_index,self.reverse)
##skip to pick up 2
       # if self.counter>=1:
           # self.pick_up_2(self.current_player_index,self.reverse,self.players, self.discard_pile,self.counter)
        #else:
        self.play_card(self.players)
##Move to the next player##
    def next_player(self, current_player_index,reverse):
        if self.reverse==False:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
        else:
            self.current_player_index = (self.current_player_index - 1) % len(self.players)
            #self.play_card(self.players)
##Pick up Cards
    def pick_up(self,current_player):
        
        print(f"{self.counter=}")
        
      
        if self.counter>=1:
            for i in range(self.counter):
                drawn_card = initial_pack.draw_card()
                current_player.hand.append(drawn_card)
                print(f"{current_player} has picked up {drawn_card}")
                #break
            self.counter=0
                
        else:
            drawn_card = initial_pack.draw_card()
            
            discarded_card_in_play = self.discard_pile[-1]
            #print(f"{discarded_card_in_play.colour}")
            #print(f"{discarded_card_in_play.number}")
            if (str(drawn_card) == "wild" or str(drawn_card) == "pick_up_4") or \
                (drawn_card.colour == discarded_card_in_play.colour) or \
                (drawn_card.number == discarded_card_in_play.number) or \
                ("pick_up_2" in str(drawn_card) and "pick_up_2" in str(discarded_card_in_play)):

            #if discarded_card_in_play.number == (drawn_card.number) or discarded_card_in_play.colour in str(drawn_card):
               # print(f"bob")
           # if discarded_card_in_play.number == (drawn_card.number) or discarded_card_in_play.colour in str(drawn_card):
                #print(f"{current_player}you have drawn a playable card, {drawn_card} do you want to play it now ?")

                while True:
                    response = input(f"{current_player} you have drawn a playable card, {drawn_card} do you want to play it now ? (yes/no): ").strip().lower()
                    if response in ["yes", "no"]:
                        break
                    else:
                        print("Please enter 'yes' or 'no'.") 
                if response == "yes":
                    self.discard_pile.append(drawn_card)
                    print(f"{current_player} has played {drawn_card}")
                    print (f"the top card on the discard pile is {self.discard_pile[-1]}")
                    self.played_card=drawn_card
                    self.check_played_card(self.played_card, current_player,self.current_player_index)
                else:
                  current_player.hand.append(drawn_card)
                  print(f"{current_player} has picked up {drawn_card}") 
            else:
                current_player.hand.append(drawn_card)
                print(f"{current_player} has picked up {drawn_card}")

##concurent pick up 2
    def pick_up_2(self,current_player_index,reverse,players, discard_pile,counter):
        #self.current_player_index+1
        print(f"the current player is {self.current_player_index+1}")
        #print(f"direction is {self.reverse}")
        
        while True:  
            current_player = self.players[self.current_player_index]
            current_player_hand = current_player.hand

            print(f"{current_player}, it is your turn, you can only play a pick_up_2 or P: {', '.join(map(str, current_player_hand))}")
                
                
            chosen_card_index = input("Enter the index of the card you want to play or enter 'P' to pick up: ")
            #drop to pick up card
            if chosen_card_index.upper() == 'P':
                self.pick_up(current_player)
                break
            
            #convert str to int
            chosen_card_index=int(chosen_card_index)
            #check int is in range
            if chosen_card_index not in range(len(current_player_hand)):
                    print("you have not chosen a valid card index.")
                    game1.pick_up_2(self.current_player_index,self.reverse,
                                    self.players, self.discard_pile,self.counter)
                    break
            played_card = current_player_hand[chosen_card_index]
            #self.discarded_card_in_play = self.discard_pile[-1]


            if "pick_up_2" in str(played_card):
                self.counter+=2
                print(self.counter)
                self.discard_pile.append(played_card)
                current_player.hand.remove(played_card)  # Remove the card from the player's hand
                #self.current_player_index = (self.current_player_index + 1) % len(self.players)
                print(f"top card on the discard pile is {played_card}")
                if self.reverse==False:
                        self.current_player_index = (self.current_player_index + 1) % len(self.players)
                else:
                        self.current_player_index = (self.current_player_index - 1) % len(self.players)
                self.pick_up_2(current_player_index,reverse,players, discard_pile,self.counter)
                break #player has played a valid card
            else:
                print("invalid card choose again")
                self.pick_up_2(current_player_index,reverse,players, discard_pile,self.counter)
                break


##check all cards###
    def check_played_card(self, played_card, current_player,current_player_index): 
                   
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
                    self.counter = 4
                    if self.reverse==False:
                        self.current_player_index = (self.current_player_index + 1) % len(self.players)
                        current_player = self.players[self.current_player_index]
                        current_player_hand = current_player.hand
                    else:
                        self.current_player_index = (self.current_player_index - 1) % len(self.players)
                        current_player = self.players[self.current_player_index]
                        current_player_hand = current_player.hand
                    self.pick_up(current_player)
                    
                    break
                else:
                    print(f"invalid colour chosen, choose again")
        
        elif "pick_up_2" in str(played_card):
            self.counter +=2
            #print(f" counter = {self.counter}")
            print(f"{self.counter=}")
            ###move to the next player
            if self.reverse==False:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
            else:
                self.current_player_index = (self.current_player_index - 1) % len(self.players)

            self.pick_up_2(self.current_player_index,self.reverse,self.players, self.discard_pile,self.counter)
            #break
            # go to next player
            #game1.pick_up(current_player)

        elif "miss_a_turn" in str(played_card):
            if self.reverse==False:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                print(f" Player {self.current_player_index+1} You miss a turn")
            else:
                self.current_player_index = (self.current_player_index - 1) % len(self.players)
                print(f" Player {self.current_player_index+1} You miss a turn")
                #self.next_player(self.current_player_index,self.reverse)
                #break
            
        elif "reverse" in str(played_card):
            self.reverse= not self.reverse # using not keyword as a flip
        
                
    #self.play_card(self.players)    
print("Game Over")
       
                

################## call things ###################
#startGame()
initial_pack.shuffle()
for shuffledcards in initial_pack.pack:  ##show shuffled pack###
    print(shuffledcards) 
game1=startGame()
game1.start_new_game()
game1.deal()
game1.discard()
game1.play_card(game1.players)
