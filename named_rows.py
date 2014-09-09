"""This file contains definitions for named rows"""

import itertools

def Rounds(n_bells):
    return tuple( range(1, n_bells+1) )

def Backrounds(n_bells):
    return tuple( range(n_bells, 0, -1) )

def Queens(n_bells):
    if n_bells % 2 != 0:
        raise Exception('Queens definition only good on even numbers of bells')
    return tuple( range(1,n_bells+1,2) + range(2,n_bells+1,2) )

def Kings(n_bells):
    if n_bells % 2 != 0:
        raise Exception('Kings definition only good on even numbers of bells')
    return tuple( range(n_bells-1,0,-2) + range(2,n_bells+1,2) )

def Tittums(n_bells):
    if n_bells % 2 != 0:
        raise Exception('Tittums definition only good on even numbers of bells')
    return tuple( itertools.chain.from_iterable(  zip(range(1, n_bells/2 + 1), range(n_bells/2 + 1, n_bells+1)) ))
