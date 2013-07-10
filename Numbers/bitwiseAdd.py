
""" add two numbers only using bitwise operations, using kogge-stoneadder
need O(lgn) bitwise ops """

def add(a, b):
    p, g, i = a ^ b, a & b, 1
    while True:
        if (g << 1) >> i == 0:
            return a ^ b ^ (g << 1)
        if ((p | g) << 2) >> i == ~0:
            return a ^ b ^ ((p | g) << 1)
        p, g, i = p & (p << i), (p & (g << i)) |g, i << 1

print ' 5 + 3 = ', add(5, 3)
