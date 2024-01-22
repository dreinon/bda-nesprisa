from random import choice, randint
from uuid import uuid4


def create_dni():
    return "".join([str(randint(0, 9)) for _ in range(8)]) + choice(
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    )
    
def uuid():
    return uuid4().hex[:15]

def choose(l: list):
    index = randint(0,len(l)-1)
    return l.pop(index)