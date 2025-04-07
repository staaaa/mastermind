from itertools import combinations_with_replacement
from random import Random
import multiprocessing

class Decoder(multiprocessing.Process):
    def __init__(self, conn):
        super().__init__()
        self.allPerms = list(combinations_with_replacement([1,2,3,4,5,6], 4))
        self.rng = Random()
        self.conn = conn
    

    def makeGuess(self):
        guess = self.allPerms[self.rng.randrange(0, len(self.allPerms)-1)]
        self.allPerms.remove(guess)
        return guess
    

    def run(self):
        while True:
            guess = self.makeGuess()
            self.conn.send(guess)
            print(f"Decoder send {guess} as guess")
            mark = self.conn.recv()
            print(f"Decoder got {mark} as mark \n")
            if mark[0] == True:
                break
        
