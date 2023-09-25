# IMPORTS
import os

line = "--"*64

def new_screen():
    os.system('cls')

class Screen:
    def __init__(self) -> None:
        # The screen is a list of lines in a list
        self.screen = []

    def update(self, line:int, output:str):
        self.screen[line] = output
    
    

