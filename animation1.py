import random
import time
import os
from colorama import Fore, Style, init
init(autoreset=True)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
score = 0
rounds = 5
print(Fore.MAGENTA + "🃏 WELCOME TO CATCH THE JOKER 🃏")
print(Fore.CYAN + "Guess the Joker's position (row & column)")
input(Fore.YELLOW + "Press Enter to start...")
for r in range(rounds):
    clear()
    size = 3
    joker_row = random.randint(0, size-1)
    joker_col = random.randint(0, size-1)
    print(Fore.GREEN + f"\nRound {r+1}")
    print(Fore.CYAN + "Grid Positions:\n")
    for i in range(size):
        for j in range(size):
            print(Fore.YELLOW + f"({i},{j})", end=" ")
        print()
    try:
        guess_row = int(input(Fore.WHITE + "\nEnter row (0-2): "))
        guess_col = int(input(Fore.WHITE + "Enter column (0-2): "))
    except:
        print(Fore.RED + "Invalid input! Skipping round...")
        time.sleep(1)
        continue
    clear()
    print(Fore.MAGENTA + "Joker was here 👇\n")
    for i in range(size):
        for j in range(size):
            if i == joker_row and j == joker_col:
                print(Fore.RED + "🃏", end=" ")
            else:
                print(Fore.BLUE + "*", end=" ")
        print()
    if guess_row == joker_row and guess_col == joker_col:
        print(Fore.GREEN + "\n😈 You caught the Joker!")
        score += 1
    else:
        print(Fore.RED + "\n😂 Joker escaped!")
    time.sleep(2)
clear()
print(Fore.MAGENTA + "🎮 GAME OVER")
print(Fore.CYAN + f"Your Score: {score}/{rounds}")
if score == rounds:
    print(Fore.GREEN + "🔥 You outsmarted the Joker!")
elif score >= 3:
    print(Fore.YELLOW + "😏 Not bad, but Joker still laughs...")
else:
    print(Fore.RED + "💀 Joker wins this time!")
