import Dominion
import random
import sys

__author__ = 'Carl-Admin'

should_print = False
ties = 0
for i in range(100):
    my_game = Dominion.Game(4,[1,2,2,2], should_print)
    if i % 500 == 0:
        print(i)
    my_game.play_game()





