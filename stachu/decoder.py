from itertools import combinations_with_replacement
from random import Random
import multiprocessing

COLOR = 2
WHITE = 1
INCORRECT = 0

class Decoder(multiprocessing.Process):
    def __init__(self, conn):
        super().__init__()
        self.allPerms = list(combinations_with_replacement([1,2,3,4,5,6], 4))
        self.rng = Random()
        self.conn = conn
        self.feedback = None
        self.previousGuess = None
        self.numbersAvailable = [1,2,3,4,5,6]

    def makeGuess(self):
        #If we haven't received any feedback to our previous guesses then choose randomly
        if self.feedback is None:
            guess = self.allPerms[self.rng.randrange(0, len(self.allPerms)-1)]
            self.allPerms.remove(guess)
        #If we have received feedback then
        else:
            marks = self.feedback
            guess = [0,0,0,0]
            remainingIndexes = [0,1,2,3]

            #Keep the old correct guesses
            #Go through every mark
            #if its 2 then rewrite previous guessed number
            for i in range(len(marks)):
                if marks[i] == COLOR:
                    guess[i] = self.previousGuess[i]
                    if i in remainingIndexes:
                        remainingIndexes.remove(i)

            #Keep numbers from whites but change indexes
            for i in range(len(marks)):
                if marks[i] == WHITE and remainingIndexes:  # Check if we have remaining indexes
                    tries = 0
                    while tries < 10:  # Prevent infinite loops
                        tries += 1
                        #generate random number 
                        if not remainingIndexes:  # Safety check
                            break
                        randomIndex = self.rng.randrange(0, len(remainingIndexes))
                        #we will pick a index[number] and check if the index is different from previous guess
                        if remainingIndexes[randomIndex] != i:
                            #if so set a guess[index[number]] to white value (change white index)
                            guess[remainingIndexes[randomIndex]] = self.previousGuess[i]
                            #remove used index from remaining indexes
                            remainingIndexes.remove(remainingIndexes[randomIndex])
                            break
            
            # Identify numbers to remove from available pool
            if self.previousGuess != None:
                numbers_to_remove = []
                
                # Find numbers that were used in previous guess but aren't COLOR or WHITE
                for i in range(len(self.previousGuess)):
                    number = self.previousGuess[i]
                    # If mark is INCORRECT, add the number to removal list
                    if marks[i] == INCORRECT and number in self.numbersAvailable:
                        numbers_to_remove.append(number)
                
                # Update available numbers list
                for num in numbers_to_remove:
                    if num in self.numbersAvailable:
                        self.numbersAvailable.remove(num)
                
                # Safety check - ensure we have numbers available
                if not self.numbersAvailable:
                    self.numbersAvailable = [1, 2, 3, 4, 5, 6]
            
            # Fill remaining positions with available numbers
            for index in remainingIndexes:
                if self.numbersAvailable:  # Check if we have numbers available
                    randomIndex = self.rng.randrange(0, len(self.numbersAvailable))
                    guess[index] = self.numbersAvailable[randomIndex]
                else:
                    # Fallback if no numbers are available
                    guess[index] = self.rng.randrange(1, 7)

        self.previousGuess = guess
        return guess
    
    def run(self):
        while True:
            # Make a guess and send it to coder
            guess = self.makeGuess()
            self.conn.send(guess)
            print(f"Decoder send {guess} as guess")
            # Wait for feedback from coder
            self.feedback = self.conn.recv()
            print(f"Decoder got {self.feedback} as feedback \n")
            # Check if all positions are correct (all 2's)
            if all(mark == COLOR for mark in self.feedback):
                break