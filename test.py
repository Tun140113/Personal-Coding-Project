import os
import time
import shutil
from datetime import datetime

width = shutil.get_terminal_size().columns

print("Welcome to Tuna BMI Calculator script".center(width))
print(("Time: " + datetime.now().strftime("%H:%M:%S")).center(width))

def goodbye_message():
    for _ in range(10000):
        print("Why don't you use our BMI calculator?")
        time.sleep(0.1)

def take_information():
    Name = str(input("Enter your name: "))
    unit = str(input("Enter your unit (m/cm/ft/in): ")).strip().lower()
    weight = float(input("Enter your weight in kg: "))
    height = float(input(f"Enter your height in {unit}: "))
    return Name, unit, weight, height

def regcognize_unit(unit, height):
    if unit == "m":
        return height
    elif unit == "cm":
        height = height / 100
    elif unit == "ft":
        height = height / 3.281
    elif unit == "in":
        height = height / 39.37
    else:
        for _ in range(10):
            os.system("cls")
            print(f"⚠ ERROR: The unit shouldn't be '{unit}'".center(width))
            print("PLEASE TRY AGAIN!".center(width))
            time.sleep(0.5)
            return None
    
def calculate_bmi(Name, weight, height):
    BMI = weight / (height ** 2) 
    BMI = round(BMI, 3)
    print("---Process complete---".center(width))
    print(f"Hi {Name}, your BMI is ~ {BMI}")
    if BMI < 18.5:
        print("You are underweight")
    elif BMI < 25:
        print("You have a normal weight")
    elif BMI < 30:
        print("You are overweight")
    else:
        print("You are obese")

    time.sleep(3)
    print("---Programm end---".center(width))
    

def main():
    ques = input("Do you want to calculate your BMI? (yes/no/bye): ").strip().lower()

    if ques == "yes":
        Name, unit, weight, height = take_information()

        height = regcognize_unit(unit, height)
        if height is None:
            return

        calculate_bmi(Name, weight, height)

    elif ques == "no":
        goodbye_message()

    elif ques == "bye":
        print("Thank you for using our script!".center(width))
        exit()

    else:
        print("Invalid input, please try again!")
    

while True:
    main()
    