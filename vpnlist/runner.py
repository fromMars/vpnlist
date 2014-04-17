import random


def a():
    x = random.randint(0, 4)
    print x
    return x

def b():
    x = random.randint(0, 4)
    print x
    return x

def c():
    x = random.randint(0, 4)
    print x
    return x

def d():
    x = random.randint(0, 4)
    print x
    return x

def e():
    x = random.randint(0, 4)
    print x
    return x

def runner(maps, start):
    next1 = start
    while True:
        room = maps[next1]
        #print "\n------------"
        next1 = room()

if __name__ == "__main__":
    maps = [a, b, c, d, e]
    runner(maps, 1)
    