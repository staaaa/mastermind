from itertools import combinations_with_replacement
from random import Random
import multiprocessing

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
        #If we haven't recived any feedback to our previous guesses then choose randomly
        if self.feedback is None:
            guess = self.allPerms[self.rng.randrange(0, len(self.allPerms)-1)]
            self.allPerms.remove(guess)
        #If we have recived feedback then
        else:
            #Colors and whites are a list of tuples {index, value}
            colors = self.feedback[1]
            whites = self.feedback[2]
            guess = [0,0,0,0]
            remainingIndexes = [0,1,2,3]

            #Keep the old correct guesses
            for color in colors:
                guess[color[0]] = color[1]
                remainingIndexes.remove(color[0])

            #Keep numbers from whites but change indexes
            for white in whites:
                while True:
                    #generate random number 
                    randomIndex = self.rng.randrange(0, len(remainingIndexes))
                    #we will pick a index[number] and check if the index is different from previous guess
                    if remainingIndexes[randomIndex] != white[0]:
                        #if so set a guess[index[niumber]] to white value (change white index)
                        guess[remainingIndexes[randomIndex]] = white[1]
                        #remove used index from remaining indexes
                        remainingIndexes.remove(remainingIndexes[randomIndex])
                        break
            
            if self.previousGuess != None:
                numbers_to_remove = []
                previous_values = self.previousGuess  
                
                # Identify numbers to remove
                for number in self.numbersAvailable:
                    if (number in previous_values and 
                        not any(color[1] == number for color in colors) and 
                        not any(white[1] == number for white in whites)):
                        numbers_to_remove.append(number)

                # Remove identified numbers so that decoder doesnt use twice incorrect numbers
                for num in numbers_to_remove:
                        if num in self.numbersAvailable:
                            self.numbersAvailable.remove(num)
            
            # Fill the rest of the remaining numbers with random guesses (but do not use the incorrect numbers)
            # That were previously used
            for index in remainingIndexes:
                randomIndex = self.rng.randrange(0, len(self.numbersAvailable))
                guess[index] = self.numbersAvailable[randomIndex]

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
            # Check if coder said it's gameover
            if self.feedback[0] == True:
                break
        
