from colors import Colors
from itertools import combinations_with_replacement
from random import Random
import multiprocessing
import time

COLOR = 2
WHITE = 1
INCORRECT = 0

# Class Coder - that's the player that's coding the password and marking the guesses
class Coder(multiprocessing.Process):
    def __init__(self, conn):
        super().__init__()
        self.password = []
        self.allCombinations = list(combinations_with_replacement([1,2,3,4,5,6], 4))
        self.rng = Random()
        self.conn = conn


    # Here we generate a single instance of password out of list of all possbile combinations
    def generatePassword(self): 
        self.password = self.allCombinations[self.rng.randrange(0, len(self.allCombinations))]


    # This method takes a guess as a parameter (sent from decoder) and marks it
    def markGuess(self, guess):
        #array for markings
        marks = [INCORRECT,INCORRECT,INCORRECT,INCORRECT]
        #in this array we place the indexes of positions we marked in first iteration
        marked = []

        #1. Mark all elements that are correct color and correctly placed
        #   Additionally, add every index that was marked to marked list
        for i in range(len(guess)):
            if guess[i] == self.password[i]:
                marks[i] = COLOR
                marked.append(i)

        #2. Create remaning array with only unmarked colors from password
        #   we do this so that we dont have a situation like this:
        #   password generated  - 1 2 3 4
        #   guess               - 1 1 9 9 
        #   we mark first 1 as 'color'
        #   the second 1 would be marked as 'white' because it would still be in password
        #   so we have to remove every marked number from password before second marking.
        remaining = [self.password[i] for i in range(len(self.password)) if i not in marked]

        #3. Mark all elements that are still in guess and havent been marked previously
        #   This way we ensure that all "colors" were marked before, and now we only
        #   mark "whites".
        for i in range(len(guess)):
            # if current number is in remaining password and this index hasn't been marked before
            if guess[i] in remaining and i not in marked:
                marks[i] = WHITE
                marked.append(i)
                remaining.remove(guess[i])
        return (marks)


    def run(self):
        # 1. Generate password
        self.generatePassword()
        print(f"Coder generated password: {self.password}")
        # 2. Run untill game hasn't finished
        while True:
            # 3. Wait to recive a guess
            guess = self.conn.recv()
            print(f"Coder got {guess} as guess")
            # Simulate time that it would take to check the guess
            time.sleep(5)
            # 4. Mark the guess and send back the result to the coder
            result = self.markGuess(guess)
            self.conn.send(result)
            print(f"Coder send {result} as mark")
            # 5. Check the first parameter in result (won: Boolean)
            if all(mark == COLOR for mark in result):
                break
        print("Decoder won")
