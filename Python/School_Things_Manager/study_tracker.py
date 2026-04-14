import os
import shutil
import time
import sys
from datetime import datetime
from prettytable import PrettyTable
import matplotlib.pyplot as plt

width = shutil.get_terminal_size().columns
# ================== CHECK FOR EXISTED ============
def checking_for_exists(subject):
    try: 
        with open("sessions.txt", "r", encoding="utf-8") as file: 
            for line in file: 
                if not line.strip():
                    continue
                
                saved_subject, _ = line.strip().split("|")
                
                if saved_subject.lower() == subject.lower():
                    return True   # 🔥 TRẢ VỀ NGAY

    except FileNotFoundError:
        return False

    return False
        
               
# ================== ADD SESSION ==================
def add_sessions():
    while True:
        print("Enter your Subject".center(width))
        subject = input(">>>").strip()
       

        if subject == "" or " " in subject:
            print("Subject must not be empty or contain spaces!")
            input()
            os.system("cls")

        if checking_for_exists(subject):
            os.system("cls")
            print("❌ Subject already exists!".center(width))
            input()
            os.system("cls")
            continue
        
        break

    while True:
        print(f"Enter time for '{subject}' (minutes)")
        try:
            minutes = int(input(">>>"))
            break
        except ValueError:
            print("Must be a number!")
            time.sleep(1)
            os.system("cls")

    with open("sessions.txt", "a", encoding="utf-8") as file:
        file.write(f"{subject}|{minutes}\n")

    print(f"Added: {subject} | {minutes} min")
    input()
    os.system("cls")

#================== DELETE ================
def del_sessions():
    try: 
        table = PrettyTable()
        table.field_names = ["Subject", "Time"]

        sessions = []
        
        with open("sessions.txt", "r", encoding="utf-8") as file: 
            for line in file: 
                if not line.strip():
                    continue

                subject, minutes = line.strip().split("|")
                sessions.append((subject, minutes))
                table.add_row([subject, int(minutes)])
            print(table)
        # Questioning user 
            del_subject = input("Enter name of subject to remove: ")


        #Resolve the list(remove)
        new_sessions = []
        found = False

        for subject, minutes in sessions: 
            if subject.lower() != del_subject.lower():
                new_sessions.append((subject, minutes))
            else: 
                found = True 
        if not found: 
            print("❌ Subject not found!")
        elif found: 
            #rewrite the file
            with open("sessions.txt", "w", encoding="utf-8") as file: 
                for subject, minutes in new_sessions:
                    file.write(f"{subject}|{minutes}\n")
            print("✅ Deleted successfully!")
    except FileNotFoundError:
        print("File doesn't exist!")
        input()

            

# ================== VIEW ==================
def view_sessions():
    try:
        table = PrettyTable()
        table.field_names = ["Subject", "Time"]

        with open("sessions.txt", "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                subject, minutes = line.strip().split("|")
                table.add_row([subject, int(minutes)])

        print(table)
        input()

    except FileNotFoundError:
        print("No data yet 😴")
        input()


# ================== STATS + GRAPH ==================
def stats():
    subjects = {}

    try:
        with open("sessions.txt", "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                subject, minutes = line.strip().split("|")
                minutes = int(minutes)

                if subject in subjects:
                    subjects[subject] += minutes
                else:
                    subjects[subject] = minutes

        if not subjects:
            print("No data for graph 😴")
            input()
            return

        x = list(subjects.keys())
        y = list(subjects.values())

        plt.bar(x, y)

        plt.title("Study Progress")
        plt.xlabel("Subjects")
        plt.ylabel("Minutes")

        plt.show()

    except FileNotFoundError:
        print("No sessions found 😭")
        input()


# ================== MENU ==================
def menu():
    while True:
        print("_____________________".center(width))
        print(("Time: " + datetime.now().strftime("%H:%M:%S")).center(width))
        print("Study Tracker".center(width))
        print("(1) Add session")
        print("(2) View sessions")
        print("(3) Show graph stats")
        print("(4) Delete sessions")
        print("(5) Exit")

        choice = input(">>> ")

        if choice == "1":
            os.system("cls")
            add_sessions()

        elif choice == "2":
            os.system("cls")
            view_sessions()

        elif choice == "3":
            os.system("cls")
            stats()
        elif choice == "4":
            os.system("cls")
            del_sessions()

        elif choice == "5":
            print("Bye 👋")
            sys.exit()

        else:
            print("Invalid choice")
            time.sleep(1)
            os.system("cls")


menu()