import Dominion
import random
import sys

__author__ = 'Carl-Admin'

should_print = False
ties = 0
my_game = Dominion.Game(4,[1,2,2,2], should_print)
for i in range(5):
    if i % 500 == 0:
        print(i)
    my_game.play_game()
    my_game.restart()





