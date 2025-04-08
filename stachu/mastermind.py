import decoder
from coder import Coder
import os
import multiprocessing

class Mastermind:
    def __init__(self):
        coder_conn, decoder_conn = multiprocessing.Pipe()
        self.coder = Coder(coder_conn)
        self.decoder = decoder.Decoder(decoder_conn)

    def initalizeGame(self):
        self.coder.start()
        self.decoder.start()

        self.coder.join()
        self.decoder.join()
