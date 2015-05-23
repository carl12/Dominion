__author__ = 'Carl-Admin'
import random


class Card:
    cost = 0
    draw = 0
    money = 0
    actions = 0
    buy = 0
    vp = 0
    name = "deffault name"
    reaction = False
    attack = False
    special = False
    is_coin = False
    is_vp = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Special_Card(Card):
    special = True
    def do_card(self, game, player, arg1, arg2):
        print("abstract method - do_card")


class Coin(Card):
    is_coin = True


class Vp(Card):
    is_vp = True


class Moat(Card):
    cost = 2
    reaction = True
    draw = 2
    name = "Moat"


class Chapel(Special_Card):
    cost = 2

    def do_card(self, game, player, arg1, arg2 = -1):
        print("Chapel needs trash")
        for i in reversed(range(len(arg1))):
           player.cards.discard_card_n(arg1[i])



    name = "Chapel"


class Cellar(Special_Card):
    cost = 2
    special = True
    name = "Cellar"
    def do_card(self, game, player, arg1, arg2):
        for i in reversed(range(len(arg1))):
            player.cards.discard_card_n(arg1[i])


class Village(Card):
    cost = 3
    draw = 1
    actions = 2
    name = "Village"


class Woodcutter(Card):
    cost = 3
    buy = 1
    money = 2
    name = "Woodcutter"


class Workshop(Special_Card):
    cost = 4

    def do_card(self, game, player, arg1, arg2):
        card = game.game_pile.card_piles[arg1]
        if card.cost <= 3:
            player.get(game,arg1)

    name = "Workshop"


class Militia(Special_Card):
    cost = 4
    attack = True
    money = 2
    name = "Militia"
    def attack(self):
        print("milita attack")

    def do_card(self, game, player, arg1, arg2):
        for i in range(len(game.players)):
            if game.players[i] is not player:
                print("ugh how do we do this")




class Smithy(Card):
    cost = 4
    draw = 3
    name = "Smithy"


class Market(Card):
    cost = 5
    draw = 1
    actions = 1
    gold = 1
    buy = 1
    name = "Market"


class Mine(Special_Card):
    cost = 5

    def do_card(self, game, player, arg1, arg2):
        card = player.cards.hand[arg1]
        if card.is_coin:
            val = card.cost
            card2 = game.game_pile.all_piles[arg2]
            if card2.cost <= val + 3:
                player.cards.trash_card_n(game.game_pile,arg1)
                player.cards.hand.append(card2)
                game.game_pile.card_remaining[arg2] -= 1

    name = "Mine"


class Remodel(Special_Card):
    cost = 4

    def do_card(self, game, player, arg1, arg2):
        card1 = player.cards.hand[arg1]
        card2 = game.game_pile.card_piles[arg2]
        if card1.cost + 2 >= card2.cost:
            player.cards.hand.trash_card_n(arg1)
            player.get(game,arg2)

    name = "Remodel"


class Copper(Coin):
    cost = 0
    money = 1
    name = "Copper"


class Silver(Coin):
    cost = 3
    money = 2
    name = "Silver"


class Gold(Coin):
    cost = 6
    money = 3
    name = "Gold"


class Estate(Vp):
    cost = 2
    vp = 1
    name = "Estate"


class Duchy(Vp):
    cost = 5
    vp = 3
    name = "Duchy"


class Province(Vp):
    cost = 8
    vp = 6
    name = "Province"


class Curse(Vp):
    cost = 0
    vp = -1
    name = "Curse"


class Collection:
    deck = []
    discards = []
    hand = []
    prints = False

    def __init__(self,prints):
        self.prints = prints
        self.deck = [Copper(), Copper(), Copper(), Copper(), Copper(),
                     Copper(), Copper(), Estate(), Estate(), Estate()]
        self.hand = []
        self.discards = []
        random.shuffle(self.deck)
        self.draw5()

    def shuffle_discard(self):
        self.deck.extend(self.discards)
        self.discards = []
        random.shuffle(self.deck)

    def draw5(self):
        for i in range(5):
            if len(self.deck) == 0:
                self.shuffle_discard()
            self.hand.append(self.deck[0])
            self.deck.pop(0)

    def drawN(self, n):
        for i in range(n):
            if len(self.deck) == 0:
                self.shuffle_discard()
            self.hand.append(self.deck[0])
            self.deck.pop(0)

    def discard_card_n(self, n):
        self.discards.append(self.hand[n])
        self.hand.pop(n)

    def trash_card_n(self,pile,n):
        pile.trash.append(self.hand[n])
        self.hand.pop(n)

    def discard_hand(self):
        self.discards.extend(self.hand)
        self.hand = []

    def has_reaction(self):
        for i in range(len(self.hand)):
            if self.hand[i].reaction:
                return True
        return False

    def get_points(self):
        a = 0
        for i in range(len(self.hand)):
            a += self.hand[i].vp
        for i in range(len(self.discards)):
            a += self.discards[i].vp
        for i in range(len(self.deck)):
            a += self.deck[i].vp
        return a


class Player:
    cards = None
    money = 0
    buys = 1
    actions = 1
    game_pile = None
    prints = False
    vp = 0

    def __init__(self, pileIn, prints = False):
        self.actions = 1
        self.buys = 1
        self.money = 0
        self.prints = prints
        self.game_pile = pileIn
        self.cards = Collection(prints)
        self.vp = 3

    def end_turn(self):
        self.cards.discard_hand()
        self.cards.draw5()
        self.money = 0
        self.buys = 1
        self.actions = 1

    def draw(self):
        self.cards.drawN(1)

    def drawN(self,n):
        self.cards.drawN(n)

    def add_treasure(self):
        for i in range(len(self.cards.hand)):
            if self.cards.hand[i].is_coin:
                self.money += self.cards.hand[i].money

    def play(self, loc):
        #print("asdfasdfasdf")
        my_card = self.cards.hand[loc]
        if self.actions == 0:
            print("Cant play b/c actions = 0")
            return
        elif my_card.special:
            print("doing special card")
        #print("playing card...")
        self.money += my_card.money
        self.buys += my_card.buy
        self.actions += my_card.actions
        if my_card.draw > 0:
            self.cards.drawN(my_card.draw)
        self.cards.discard_card_n(loc)
        self.actions -= 1

    def play_sp(self, loc, input1 = -1, input2 = -1):
        card = self.cards.hand[loc]

    def get(self,game,n):
        card = game.game_pile.all_piles[n]
        if game.game_pile.is_remaining(n):
            self.cards.discards.append(card)
            self.vp += card.vp

    def buy(self, game, n):
        card = game.game_pile.card_piles[n]
        if self.money >= card.cost and self.buys > 0:
            if game.game_pile.is_remaining(n):
                self.buys -= 1
                self.money -= card.cost
                self.cards.discards.append(card)
                self.vp += card.vp

    def get_points(self):
        return self.cards.get_points()


class Piles:
    card_piles = []
    card_remaining = []
    card_loc = []
    building_loc = {}

    exhausted_piles = 0
    trash = []
    default_buildings = [Cellar(), Moat(), Village(), Woodcutter(), Workshop(), Militia(), Remodel(), Smithy(), Market(),
                     Mine()]
    default_loc = {"Cellar": 0, "Moat": 1, "Village": 2, "Woodcutter": 3, "Workshop": 4, "Militia": 5, "Remodel": 6,
                   "Smithy": 7, "Market": 8, "Mine": 9,
                   "Copper":10,"Silver":11,"Gold":12,
                   "Estate":13,"Duchy":14,"Province":15,"Curse":16}

    def __init__(self, player_num, buildings = default_buildings,):

        self.card_remaining = []
        self.card_piles = buildings.copy()
        for x in range(len(buildings)):
            self.building_loc[buildings[x].name] = x
            self.card_remaining.append(10)

        self.card_piles.extend([Copper(), Silver(), Gold()])
        self.card_remaining.extend([100,100,100])

        self.card_piles.extend([Estate(), Duchy(), Province(),Curse()])
        self.vp_num = player_num * 4

        self.card_remaining.append(self.vp_num)
        self.card_remaining.append(self.vp_num)
        self.card_remaining.append(self.vp_num)

        self.card_remaining.append(player_num * 5)

        self.exhausted_piles = 0

    def is_remaining(self, n):
        if self.card_remaining[n] > 0:
            self.card_remaining[n] -= 1
            if self.card_remaining == 0:
                self.exhausted_piles += 1
            return True
        return False


class Game:
    players = []
    ais = []
    curr_player = -1
    game_pile = None
    round = 0
    finished = False

    def __init__(self, players,prints):
        self.game_pile = Piles(players)
        self.players = []
        self.round = 0
        for i in range(players):
            self.players.append(Player(self.game_pile,prints))
        self.curr_player = 0

    def setAis(self, ais):
        self.ais = ais

    def do_militia(self, play_num):
        for i in range(len(self.players)):
            if i is not play_num:
                self.ais[i].do_militia()


    def end_turn(self):
        self.players[self.curr_player].end_turn()
        if self.check_game_over():
            return
        if self.curr_player < len(self.players) - 1:
            self.curr_player += 1
        else:
            self.curr_player = 0
            self.round += 1

    def check_game_over(self):
        if self.game_pile.exhausted_piles >= 3:
            print("Ran out of 3 piles")
            self.finished = True
        elif self.game_pile.card_remaining[15] == 0:
            print("Out of Provinces")
            self.finished = True
        elif self.round >= 100:
            print("game went to 100 rounds")
            self.finished = True
        return self.finished

    def get_points(self):
        arr = []
        for i in range(len(self.players)):
            arr.append(self.players[i].get_points())

        return arr

    def get_winner(self):
        if self.finished:
            max = -1
            loc = -1
            a = self.get_points()
            for i in range(len(a)):
                if a[i] > max:
                    max = a[i]
                    loc = i
                elif a[i] == max:
                    loc = -1

            return loc
        return -2



