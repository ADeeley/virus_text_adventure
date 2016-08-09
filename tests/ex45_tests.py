from nose.tools import *
from ex45.game import *

    
def test_basic():
    a_map = Map('intro')
    a_game = Engine(a_map)
    a_game.play()