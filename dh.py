import random
from mod import add, divide, modInv, mul

# g, p ==> 2048 bits long
pubParams = (2, 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF)

class DiffieHellman:
    def __init__(self, g: int, p: int):
        self.g = g # generator
        self.p = p # mod
        self.privKey = random.randint(1, p - 1) # privKey
    
    def getPublicKey(self):
        return pow(self.g, self.privKey, self.p)

    def update(self, otherPubKey):
        return pow(otherPubKey, self.privKey, self.p)

if __name__ == "__main__":
    # private keys
    alice = DiffieHellman(pubParams[0], pubParams[1])
    bob = DiffieHellman(pubParams[0], pubParams[1])
    print(f"[+] Alice's private key:\n\thex: {hex(alice.privKey)[2:]}\n")
    print(f"[+] Bob's private key:\n\thex: {hex(bob.privKey)[2:]}\n")

    # public keys
    alicePubKey = alice.getPublicKey()
    bobPubKey = bob.getPublicKey()
    print(f"[+] Alice's private key:\n\thex: {hex(alicePubKey)[2:]}\n")
    print(f"[+] Bob's private key:\n\thex: {hex(bobPubKey)[2:]}\n")

    # shared secret
    sharedSecretAlice = alice.update(bobPubKey)
    sharedSecretBob = bob.update(alicePubKey)
    print(f"[+] SharedSecret:\n\thex: {hex(sharedSecretAlice)[2:]}\n")
    print(f"[+] SharedSecret Match: {sharedSecretBob == sharedSecretAlice}\n")