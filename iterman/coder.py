#!/usr/bin/env python3
import time
from random import randint
import multiprocessing

COLOR = 2
WHITE = 1
INCORRECT = 0

class Coder(multiprocessing.Process):
    """
    Klasa Coder generuje hasło i porównuje próby zgadywania z hasłem.
    """
    def __init__(self, conn):
        """Inicjalizuje proces"""
        super().__init__()
        self.conn = conn
        self.password = []

    def generate_password(self):
        """Losuje hasło"""
        for _ in range(4):
            self.password.append(randint(1, 6))

    def evaluate_guess(self, guess):
        """
        Porównuje zgadnięcie z hasłem i zwraca wynik jako listę ocen.
        2 - trafiony kolor na właściwym miejscu,
        1 - trafiony kolor, ale na złej pozycji,
        0 - nietrafiony kolor.
        """

        evaluation = [INCORRECT] * 4
        remaining = []

        for i in range(4):
            if guess[i] == self.password[i]:
                evaluation[i] = COLOR
            else:
                remaining.append(self.password[i])

        for i in range(4):
            if evaluation[i] == INCORRECT and guess[i] in remaining:
                evaluation[i] = WHITE
                remaining.remove(guess[i])

        return evaluation

    def run(self):
        """Główna pętla procesu Coder: generuje hasło i ocenia zgadnięcia otrzymywane przez pipe."""

        self.generate_password()

        print(f"[Coder] Generated password: {self.password}")

        while True:
            guess = self.conn.recv()
            result = self.evaluate_guess(guess)

            time.sleep(3)
            self.conn.send(result)
            print(f"[Coder] Sent feedback: {result}")

            if result == [COLOR, COLOR, COLOR, COLOR]:
                break
        print("[Coder] Decoder won!")
