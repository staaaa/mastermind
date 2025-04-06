from itertools import combinations
from random import Random
import multiprocessing

class Decoder(multiprocessing.Process):
    def __init__(self, conn):
        super().__init__()
        self.allPerms = list(combinations([1,2,3,4,5,6], 4))
        self.rng = Random()
        self.conn = conn
    

    def makeGuess(self):
        return self.allPerms[self.rng.randrange(0, len(self.allPerms)-1)]
    

    def run(self):
        while True:
            guess = self.makeGuess()
            self.conn.send(guess)
            print(f"Decoder send {guess} as guess")
            mark = self.conn.recv()
            print(f"Decoder got {mark} as mark")
            if mark[0] == True:
                break
        
