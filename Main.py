import Dominion
import random
import sys
a = "3.2"
b = "3"
c = "-3"
print(a.isdigit(), b.isdigit(),c.isnumeric())
__author__ = 'Carl-Admin'

should_print = False
ties = 0
print(Dominion.ai_type)
my_game = Dominion.Game(4,[0,2,2,2], should_print)
for i in range(1):
    my_game.restart()
    if i % 500 == 0:
        print(i)
    my_game.play_game()
    print(my_game.get_points())







