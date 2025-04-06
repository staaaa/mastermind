from colors import Colors
from itertools import combinations
from random import Random
import multiprocessing
import time

class Coder(multiprocessing.Process):
    def __init__(self, conn):
        super().__init__()
        self.password = []
        self.allPerms = list(combinations([1,2,3,4,5,6], 4))
        self.rng = Random()
        self.conn = conn


    def generatePassword(self): 
        self.password = self.allPerms[self.rng.randrange(3, len(self.allPerms))]


    def markGuess(self, guess):
        colors = 0
        whites = 0
        won = False
        marked = []

        for i in range(len(guess)):
            if guess[i] == self.password[i]:
                colors += 1
                marked.append(i)
        for i in range(len(guess)-1):
            if i not in marked and guess[i] in self.password:
                whites += 1
                marked.append(i)
        if colors == 4:
            won = True
        return (won, colors, whites)


    def run(self):
        #wait to recive the guess
        self.generatePassword()
        print(f"Coder generated password: {self.password}")
        while True:
            guess = self.conn.recv()
            print(f"Coder got {guess} as guess")
            time.sleep(5)
            mark = self.markGuess(guess)
            self.conn.send(mark)
            print(f"Coder send {mark} as mark")
            if mark[0] == True:
                break
        print("Decoder won")
