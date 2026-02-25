import os 
import shutil
import time
from datetime import datetime

width = shutil.get_terminal_size().columns
os.system("cls")

print("Welcome to our Mini Data Analyzer".center(width))
print("1 .Please choose your option: ")
print("2. Find the highest point ")
print("3. Find the lowest point ")
print("4. Find the average: ")
print("uhh, quit:  ")



def findthehighest():
    try: 
        raw_input_score = input("Please enter raw score, split with 'space' : ")
        score_list = raw_input_score.split()
        

        score = []
        for item in score_list:
            score.append(int(item))
        highest = score_list[0]
        if not score:   
            print("No data to analyze")
            return

        else:
            print(score)

    except IndexError:
        print("No data to analyze")
        return

findthehighest()