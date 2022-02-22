from math import sqrt

def solve_eq(b, c):
    v1 = b
    v2 = v1 * v1
    v3 = v2 + c
    v4 = sqrt(v3)
    return v4 - v1

print(solve_eq(10, 39))

def AND(a, b): return a * b
def OR(a, b):  return 1 if a + b else 0
def NOT(a):    return 1 - a
def XOR(a, b):
    """proof by python"""
    w2 = NOT(AND(a, b)) # a = b = 1
    w3 = OR(a, b)       # a = b = 0
    return AND(w2, w3)

def XOR3(a, b, c): return XOR(XOR(a, b), c)
def NAND(a, b):
    return NOT(AND(NOT(AND(a, b)), NOT(AND(a, b)))) or \
           NOT(AND(NOT(AND(a, a)), NOT(AND(b, b)))) or \
           NOT(AND(NOT(a), NOT(b)))                 or \
           NOT(AND(a, a))

def ALLEQ(a, b, c, d):
    reg = AND(AND(AND(a, b), c), d)
    return OR(reg, NOT(reg))

print(["XOR3(" + str(a) + ", " + str(b) + ", " + str(c) + ") = " + str(XOR3(a, b, c)) for a in [0, 1] for b in [0, 1] for c in [0,1]])
print([f"XOR({a}, {b}) = {XOR(a, b)}" for a in [0, 1] for b in [0, 1]])
print("ALLEQ(1, 1, 1, 1) =", "true" if ALLEQ(1, 1, 1, 1) else "false")

def MAJ(X, Y, Z):
    firstpair  = AND(X, Y)
    secondpair = AND(Y, Z)
    thirdpair  = AND(X, Z)
    temp       = OR(secondpair, thirdpair)
    return OR(firstpair, temp)

print("MAJ(0, 1, 1) = ", MAJ(0, 1, 1))

def BOOLEAN_CIRCUIT(X: tuple):
    layer: list  # list of the minimal layering
    output: list # list of outputs
    gate = { "^": AND, "v": OR, "~": NOT } # list of logic gates

    for i, v in enumerate(layer):
        if v in X: # v is an input vertex
            v = X[i]
        elif v in gate: # v is a gate
            match gate[v]:
                case "^":
                    v = AND(X[i-1], X[i])
                case "v":
                    v = OR(X[i-1], X[i])
                case "~":
                    v = NOT(X[i])

            if v in output: # v is an output C(v)
                return v

def CMP(X: tuple):
    """
    outputs true if (a, b) > (c, d) iff
    a > c OR (a >= c AND b > d)
    """
    # check if c1 > c2
    t1 = NOT(X[2])
    t2 = AND(X[0], t1)
    # check if c1 >= c2
    t3 = OR(X[0], t1)
    # check if b > d
    t4 = NOT(X[3])
    t5 = AND(X[1], t4)
    # compute a >= c AND b > d
    t6 = AND(t5, t3)

    Y[0] = OR(t2, t6)
