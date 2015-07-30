import sys

class Ai:
    player_num = -1
    player = None
    game = None
    prints = False
    vps = 3
    vp_cards = [0, 0, 0]

    def __init__(self, player_num, game, prints=False):
        self.vp_cards = [3, 0, 0]

        self.prints = prints
        self.player_num = player_num
        print(player_num)
        self.player = game.players[player_num]
        self.game = game

    def do_turn(self):
        print("should be abstract...")

    def do_militia(self):
        print('Doing discarding from ai')
        self.player.cards.discard(1)
        self.player.cards.discard(0)


class BM_64_Basic(Ai):
    wins = [0]
    prov = 0
    name = "coin"
    duchy = 6
    estate = 4

    def __init__(self, player_num, game, duchy=6, estate=4, prints=False):
        super(BM_64_Basic, self).__init__(player_num, game, prints=False)
        self.duchy = duchy
        self.estate = estate

        self.prov = 0

    def restart_ai(self):
        self.prov = 0
        self.player = self.game.players[self.player_num]


    def do_turn(self):
        prov_rem = self.game.game_pile.card_remaining[15]
        points = self.game.get_points()

        max_points = -1
        loc = -1
        for i in range(len(points)):
            if points[i] > max_points:
                max_points = points[i]
                loc = i
        diff = points[loc] - points[self.player_num]
        self.player.add_treasure()
        money = self.player.money

        if prov_rem <= 1:
            if money >= 8 and diff <= 6:
                self.player.buy(self.game, 15)
                self.vp_cards[2] += 1
            elif money >= 5:
                self.vp_cards[1] += 1
            elif money >= 2:
                self.player.buy(self.game, 13)

                self.vp_cards[0] += 1
        elif prov_rem <= self.estate:
            if money >= 8:
                self.player.buy(self.game, 15)
                self.vp_cards[2] += 1
            elif money >= 5:
                self.player.buy(self.game, 14)

                self.vp_cards[1] += 1
            elif money >= 2:
                self.player.buy(self.game, 13)

                self.vp_cards[0] += 1
        elif prov_rem <= self.duchy:
            if money >= 8:
                self.player.buy(self.game, 15)

                self.vp_cards[2] += 1
            elif money >= 5:
                self.player.buy(self.game, 14)

                self.vp_cards[1] += 1
            elif money >= 3:
                self.player.buy(self.game, 11)
        elif money >= 8:
            self.player.buy(self.player, 15)
            self.prov += 1

            self.vp_cards[2] += 1
        elif money >= 6:
            self.player.buy(self.game, 12)
        elif money >= 3:
            self.player.buy(self.game, 11)

        def do_militia(self):
            for i in reversed(range(self.player.cards.hand)):
                if len(self.player.cards.hand) == 3:
                    return
                if self.player.cards.hand[i].is_vp:
                    self.player.cards.discard(i)
            for i in reversed(range(self.player.cards.hand)):
                if len(self.player.cards.hand) == 3:
                    return
                if self.player.cards.hand[i].name == "Copper":
                    self.player.cards.discard(i)
            for i in reversed(range(self.player.cards.hand)):
                if len(self.player.cards.hand) == 3:
                    return
                if self.player.cards.hand[i].name == "Silver":
                    self.player.cards.discard(i)
            print("Couldnt find anything to discard")
            print(self.player.cards.hand)
            print()
            print()
            print()


class BMSmithy(Ai):
    wins = [0]
    prov = 0
    curr_smithy = 0
    ideal_smithy = 1
    name = "smithy"
    prints = True


    def restart_ai(self):
        self.player = self.game.players[self.player_num]
        self.curr_smithy = 0
        self.prov = 0

    def do_turn(self):
        loc = self.has_smithy()
        if loc >= 0:
            self.player.play(loc)
        self.player.add_treasure()
        money = self.player.money
        if money >= 8:
            self.player.buy(self.player, 15)

            self.prov += 1
            self.vp_cards[2] += 1
        elif money >= 6:
            self.player.buy(self.player, 12)
        elif money >= 4 and self.curr_smithy < self.ideal_smithy:
            self.player.buy(self.player, 7)
            self.curr_smithy += 1
        elif money >= 3:
            self.player.buy(self.player, 11)

    def has_smithy(self):
        hand = self.player.cards.hand
        for i in range(len(hand)):
            if hand[i].name == "Smithy":
                return i
        return -1

    def do_militia(self):
        for i in reversed(range(self.player.cards.hand)):
            if len(self.player.cards.hand) == 3:
                return
            if self.player.cards.hand[i].is_vp:
                self.player.cards.discard(i)
        for i in reversed(range(self.player.cards.hand)):
            if len(self.player.cards.hand) == 3:
                return
            if self.player.cards.hand[i].name == "Copper":
                self.player.cards.discard(i)
        for i in reversed(range(self.player.cards.hand)):
            if len(self.player.cards.hand) == 3:
                return
            if self.player.cards.hand[i].name == "Smithy":
                self.player.cards.discard(i)
        for i in reversed(range(self.player.cards.hand)):
            if len(self.player.cards.hand) == 3:
                return
            if self.player.cards.hand[i].name == "Silver":
                self.player.cards.discard(i)

        print("Couldnt find anything to discard")
        print(self.player.cards.hand)
        print()
        print()
        print()


class Person(Ai):
    wins = 0
    def restart_ai(self):
        self.player = self.game.players[self.player_num]

    def do_turn(self):
        print("________________________________")
        print("It is now your turn!")
        print_game_state(self.game, self.player)
        while self.player.actions > 0:
            print("________________________________")
            hand = self.player.cards.hand
            print("Your hand: ", hand)
            if has_action(hand):
                print("Which card would you like to play? You have", self.player.actions, "actions \n"
                    " (0 to", len(hand) - 1, ") enter -1 to count treasure and buy")
            else:
                print("You have no actions cards available, jumping to buy phase")
                break
            playLoc = int(sys.stdin.readline())
            if playLoc == -1:
                break
            elif playLoc < len(hand):
                played_card = hand[playLoc]
                if played_card.is_coin:
                    print("That's a coin")
                elif played_card.is_vp:
                    print("That's a vp card")
                elif played_card.special:
                    played_card.user_prompt(self.player)
                else:
                    print("playing...", played_card)
                    print(self.player.actions)
                    self.player.play(playLoc)

        self.player.add_treasure()
        while self.player.buys > 0:
            print("________________________________")
            print("What do you want to buy? You have", self.player.buys, "buys and ", self.player.money, "money")
            b = int(sys.stdin.readline())
            if b == -1:
                break
            elif b < len(self.game.game_pile.card_piles):
                card_to_buy = self.game.game_pile.card_piles[b]
                if card_to_buy.cost <= self.player.money:
                    self.player.buy(self.game, b)
                    print("You bought a", self.game.game_pile.card_piles[b])
        print("Turn over")
        print("________________________________")

    def do_militia(self):
        hand = self.player.cards.hand
        print("________________________________")
        print("Milita played")
        while True:
            print(hand)
            print("play a reaction card or -1")
            play = int(sys.stdin.readline())
            if play == -1:
                break;
            elif hand[play].reaction:
                if hand[play].name == "Moat":
                    print("You played a moat")
                    return;
                else:
                    print("not a moat")
        while len(hand) > 3:
            hand = self.player.cards.hand
            print("Discard cards down to 3 cards")
            print(hand)
            discard = int(sys.stdin.readline())
            print("Discarding ", hand[discard])
            self.player.cards.discard(discard)


def has_action(hand):
    for i in range(len(hand)):
        if not hand[i].is_coin and not hand[i].is_vp:
            return True
    return False


def print_game_state(game, player):
    pile = game.game_pile.card_piles
    remain = game.game_pile.card_remaining
    for i in range(len(pile)):
        print(pile[i].name, i, ":", remain[i], end="| ")
        if i % 3 == 2:
            print()
    print()
    print()
    print("There are", len(player.cards.discards), "cards in your discard")
    print("There are", len(player.cards.deck), "cards in your deck")
