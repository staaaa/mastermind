#!/usr/bin/env python3
import multiprocessing
from coder import Coder
from decoderLib import Decoder

class Mastermind:
    """
    Klasa Mastermind uruchamia grę jako dwa procesy komunikujące się za pomocą pipe.
    """
    def __init__(self):
        """Inicjalizuje komunikację oraz tworzy instancje procesów Coder i Decoder."""
        coder_conn, decoder_conn = multiprocessing.Pipe()
        self.coder = Coder(coder_conn)
        self.decoder = Decoder(decoder_conn)

    def initialize_game(self):
        """Uruchamia procesy i oczekuje na ich zakończenie."""
        self.coder.start()
        self.decoder.start()
        self.coder.join()
        self.decoder.join()

if __name__ == '__main__':
    game = Mastermind()
    game.initialize_game()
