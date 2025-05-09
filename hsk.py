import random
import unicodedata
from tkinter import *

# gets the hsk data from the files and seperates them based on 
def get_hsk_data(level: int) -> dict:
    try:
        with open(f'files/hsk{level}.txt','r', encoding ='utf-8') as f:
            words = []
            for x in f:
                data = x.strip('\n').split('\t')
                words.append(data)
        return {
            'simplified': [i[0] for i in words],
            'traditional': [i[1] for i in words],
            'tone': [i[2] for i in words],
            'pinyin': [i[3] for i in words],
            'definition': [i[4] for i in words]
        }
    except FileNotFoundError:
        raise FileNotFoundError

def create_quiz(data: dict, count: int) -> list:
    return random.sample(range(len(data['simplified'])),count)

# strips the tones off of the pinyin characters using the unicode module --- looked online to figure out how to use it
def strip_tones(pinyin: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', pinyin)
                    if unicodedata.category(c) != 'Mn')
    
# Function to bind scroll to Mousewheel --- watched a tutorial on how to implement it-------# 
def on_configure(canvas)  -> None: 
    def handler(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
    return handler

def on_mousewheel(canvas)-> None:
    def handler(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    return handler
#------------------------------------------------------------------------------------------#
