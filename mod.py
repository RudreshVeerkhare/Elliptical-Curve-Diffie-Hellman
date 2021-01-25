def modInv(a, M):
    return pow(a, M-2, M)

def add(a, b, mod):
    return (a%mod + b%mod)%mod

def mul(a, b, mod):
    return ((a%mod)*(b%mod))%mod

def divide(a, b, mod):
    return mul(a, modInv(b, mod), mod)