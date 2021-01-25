from mod import add, divide, modInv, mul
from curves import CURVE_REGESTERY
import random
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x: {self.x} y: {self.y})"

class EllipticalCurves:
    def __init__(self, p: int, a: int, b: int, g: Point):
        self.mod = p
        self.a = a
        self.b = b
        self.g = g

    @staticmethod
    def addPoints(p1: Point, p2: Point, mod):
        if(p1.x == p2.x and p1.y != p2.y):
            print("Intersection at Infinity found")
        # slope = ((y2 - y1)/(x2 - x1)) % mod
        slope = divide(add(p2.y, -1*p1.y, mod), add(p2.x, -1*p1.x, mod), mod)
        x = add(mul(slope, slope, mod), -1*add(p1.x, p2.x, mod), mod)
        y = add(mul(slope, p1.x - x, mod), -1*p1.y, mod)
        return Point(x, y)


    def doublePoint(self, p: Point):
        mod = self.mod
        # slope = ((y2 - y1)/(x2 - x1)) % mod
        slope = divide(add(mul(3, pow(p.x, 2, mod), mod), self.a, mod), mul(2, p.y, mod), mod)
        x = add(mul(slope, slope, mod), -1*add(p.x, p.x, mod), mod)
        y = add(mul(slope, p.x - x, mod), -1*p.y, mod)
        return Point(x, y)
    

    def f(self, p: Point, n: int):
        if n == 1:
            return p
        elif n % 2 == 1:
            return self.addPoints(p, self.f(p, n - 1), self.mod)
        else:
            return self.f(self.doublePoint(p), n >> 1)

    def getPublicKey(self, n):
        return self.f(self.g, n)

    @staticmethod
    def compressKey(p: Point):
        return '0' + str(2 + p.y % 2) + str(hex(p.x)[2:])

    def __str__(self):
        return (f"[+] p:\n\thex: {hex(self.mod)[2:]}\n\tint: {self.mod}\n"+
                f"[+] Curve:\n\ty^2 = x^3 + {self.a}x + {self.b}\n"+
                f"[+] g:\n\tx: {self.g.x}\n\ty: {self.g.y}")


class EllipticalCurveDiffieHellman(EllipticalCurves):
    def __init__(self, p, a, b, g, privKey=None):
        super().__init__(p, a, b, g)
        if privKey: 
            self.privKey = privKey
        else:
            self.privKey = random.randint(1, p - 1)
        
    def update(self, otherPubKey):
        return self.f(otherPubKey, self.privKey)




if __name__ == "__main__":


    # brainpoolP256r1
    p = CURVE_REGESTERY["brainpoolP256r1"]["p"]
    a = CURVE_REGESTERY["brainpoolP256r1"]["a"]
    b = CURVE_REGESTERY["brainpoolP256r1"]["b"]
    g = Point(
            CURVE_REGESTERY["brainpoolP256r1"]["g"][0],
            CURVE_REGESTERY["brainpoolP256r1"]["g"][1]
        )


    alice = EllipticalCurveDiffieHellman(p, a, b, g)
    bob = EllipticalCurveDiffieHellman(p, a, b, g)
    print(alice)

    # privKey
    print(f"[+] Alice's privKey:\n\thex: {hex(alice.privKey)[2:]}\n\tint: {alice.privKey}")
    print(f"[+] Bob's privKey:\n\thex: {hex(bob.privKey)[2:]}\n\tint: {bob.privKey}")

    # pubKey
    alicePubKey = alice.getPublicKey(alice.privKey)
    bobPubKey = bob.getPublicKey(bob.privKey)
    print(f"[+] Alice's pubKey:\n\tx: {alicePubKey.x}\n\ty: {alicePubKey.y}")
    print(f"[+] Bob's pubKey:\n\tx: {bobPubKey.x}\n\ty: {bobPubKey.y}")

    
    # Shared Secret
    aliceSharedSecret = EllipticalCurves.compressKey(alice.update(bobPubKey))
    bobSharedSecret = EllipticalCurves.compressKey(bob.update(alicePubKey))
    print(f"[+] Alice's Shared Secret:\n\t{aliceSharedSecret}")
    print(f"[+] Bob's Shared Secret:\n\t{bobSharedSecret}")
    print(f"[+] Shared Secret Match:\n\t{aliceSharedSecret == bobSharedSecret}")