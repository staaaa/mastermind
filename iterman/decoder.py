#!/usr/bin/env python3

import time
import multiprocessing
from itertools import product
from copy import deepcopy

COLOR = 2
WHITE = 1
INCORRECT = 0

class Decoder(multiprocessing.Process):
    """
    Klasa Decoder korzysta z algorytmu minimax do odgadywania tajnego kodu.
    """
    def __init__(self, conn, code_length=4, color_range=(1, 7)):
        """
        Inicjalizuje proces Decoder, tworzy zbiór wszystkich możliwych kodów oraz ustala początkowy strzał,
        najlepszy wg teorii Donalda Knutha
        """
        super().__init__()
        self.conn = conn
        self.code_length = code_length
        self.color_range = color_range
        self.all_codes = [list(code) for code in product(range(color_range[0], color_range[1]), repeat=code_length)]
        self.possible_codes = deepcopy(self.all_codes)
        self.guess = [1, 1, 2, 2]

    def get_feedback(self, secret, guess):
        """
        Oblicza feedback porównując kod 'guess' z tajnym kodem 'secret'.
        Zwraca listę, w której:
          2 oznacza trafienie (właściwy kolor i pozycja),
          1 oznacza trafiony kolor, lecz złe miejsce,
          0 oznacza nietrafiony kolor.
        """
        feedback = [INCORRECT] * self.code_length
        secret_copy = secret.copy()
        guess_copy = guess.copy()
        for i in range(self.code_length):
            if guess_copy[i] == secret_copy[i]:
                feedback[i] = COLOR
                secret_copy[i] = None
                guess_copy[i] = None
        for i in range(self.code_length):
            if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                feedback[i] = WHITE
                indeks = secret_copy.index(guess_copy[i])
                secret_copy[indeks] = None
        return feedback

    def filter_possible_codes(self, guess, feedback):
        """
        Redukuje zbiór możliwych kodów do tych, które przy zgadywaniu 'guess' dają feedback równy podanemu.
        """
        self.possible_codes = [code for code in self.possible_codes if self.get_feedback(code, guess) == feedback]

    def minimax_guess(self):
        """
        Dla każdego możliwego kandydata (kodu) oblicza najgorszy możliwy przypadek,
        czyli maksymalną liczbę kodów ze zbioru możliwych odpowiedzi (possible_codes),
        które pozostałyby po zastosowaniu danego kandydata.
        
        Następnie wybiera tego kandydata, który minimalizuje ten najgorszy przypadek (worst case).
        Dzięki temu maksymalizuje postęp zgadywania w najgorszym możliwym scenariuszu.
        """

        best_score = None      # Przechowuje najlepszy wynik (czyli minimalny worst-case)
        best_guess = None      # Przechowuje kandydata z najlepszym worst-case

        # Iterujemy po wszystkich możliwych kodach (nie tylko tych, które są jeszcze możliwe jako odpowiedź)
        for candidate in self.all_codes:
            score_counts = {}  # Słownik: klucz = feedback, wartość = ile kodów da taki feedback

            # Dla każdej możliwej tajnej kombinacji (hasła, które zostały) sprawdzamy, jaki feedback dostalibyśmy, zgadując 'candidate'
            for possible in self.possible_codes:
                # Porównanie: możliwe hasło vs kandydat
                feedback = tuple(self.get_feedback(possible, candidate))  
                # Zwiększamy licznik dla danego feedbacku
                score_counts[feedback] = score_counts.get(feedback, 0) + 1

            # Najgorszy przypadek dla danego kandydata:
            # Zakładamy, że po danym zgadywaniu otrzymamy taki feedback, który zostawi nam największą liczbę możliwych kodów,
            # tym jest właśnie worst-case
            worst_case = max(score_counts.values()) if score_counts else 0

            # Teraz porównujemy, czy ten kandydat jest lepszy niż dotychczasowy najlepszy
            if best_score is None or worst_case < best_score:
                best_score = worst_case
                best_guess = candidate
            elif worst_case == best_score:
                # W przypadku remisu — mamy kilka równie dobrych kandydatów

                # Preferuj zgadywanie, które JEST w zbiorze możliwych kodów (czyli potencjalnie może być poprawne)
                if candidate in self.possible_codes and best_guess not in self.possible_codes:
                    best_guess = candidate

                # Jeśli oba są (lub oba nie są) w zbiorze możliwych – wybierz w kolejnośći leksykograficznej 
                elif ((candidate in self.possible_codes and best_guess in self.possible_codes) or
                    (candidate not in self.possible_codes and best_guess not in self.possible_codes)):
                    if tuple(candidate) < tuple(best_guess):
                        best_guess = candidate

                # Dodatkowy warunek – jeśli wszystko inne równe, i ten ma mniejszy kod numerycznie – też go wybieramy
                elif tuple(candidate) < tuple(best_guess):
                    best_guess = candidate

        return best_guess

    def run(self):
        """
        Główna pętla procesu Decoder: wysyła zgadywania, odbiera feedback, aktualizuje zbiór możliwych kodów,
        a następnie wybiera kolejne zgadywanie metodą minimax.
        """

        attempts = 0
        max_attempts = 12 # max. liczba prób

        while attempts < max_attempts:
            time.sleep(3)
            self.conn.send(self.guess)
            print(f"[Decoder] Sent guess: {self.guess}")
            feedback = self.conn.recv()

            if feedback == [COLOR, COLOR, COLOR, COLOR]:
                print("[Decoder] Code cracked!")
                break

            self.filter_possible_codes(self.guess, feedback)
            self.guess = self.minimax_guess()

            attempts += 1

        if attempts >= max_attempts:
            print("[Decoder] Maximum attempts reached. Game over.")
