# Build a coffee shop baeista robot
# First python program following NetworkChuck youtube lesson.
# I did make a few changes from the walk thought he gave.
# TheBigD 03/04/2022.

# Setup
import datetime
import os
import sys
import random
from tabulate import tabulate
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)
now = datetime.datetime.now()
hour = now.hour

# Generate the robot number for this run
robot_num = random.randint(1, 100)
robot_name = 'Robot'+str(robot_num)

# Clear the terminal screen
os.system('clear')

# Set up menu and cost lists
menu = [["1", "Regular Octain Black Coffee", 2.25],
        ["2", "Cupachino", 7.45],
        ["3",  "Cafe Americana", 3.25],
        ["4", "Mocca Grande with 2 shots", 8.59],
        ["5", "High Octane Coffee", 9.00],
        ["6", "Espresso", 3.50],
        ["7", "Green Tea", 3.25],
        ["8", "Black Leaf Tea", 3.00],
        ["9", "Premium Oolong Tea", 3.50],
        ["10", "The Pickard", 3.75]
        ]

# List of persons that have been banned from the store.
bannedList = ['ben', 'benjamin']

# Determine time of day
if hour < 12:
    greatings = 'Good morning'
    day_type = 'morning'
elif hour < 18:
    greatings = 'Good afternoon'
    day_type = 'afternoon'
else:
    greatings = "Good evening"
    day_type = 'evening'

# Store greatings
print(f"{Fore.YELLOW}{Back.BLUE}\nHello, Welcome to Gitta High Coffee Shop.")
print(f"{Fore.YELLOW}{Back.BLUE}   Where your high is just a sip away!   \n")

# Introductions
name = input(
    f"\n{greatings}. My name is {robot_name}. May I have your name plaese? ")

# Check to see if this customer has been banned
if name.casefold() in bannedList:
    print(f"{Fore.RED}{Back.YELLOW}\nOh, you're {name}!")
    print(f"{Fore.RED}{Back.YELLOW}\nYou have been baned from this establishment.\n\nPlease leave now or I will be forced to call the police\n")
    exit(f"{Back.GREEN}{Fore.BLACK}\n\nAssHat!\n\n")
else:
    print(
        f"\nHello, {name}, hope you are having a nice {day_type}.\nHere is our menu for this {day_type}:\n")

# Lets print the menu for the customer
print(tabulate(menu, headers=['No', 'Item', "Price"], floatfmt=".2f"))

# Determine what the customer would like from the menu
item = 15
while item not in range(1, 11):
    item = int(input("\nPlease enter your menu choice: "))
else:
    qty = int(input("\nHow meny would you like: "))

# Store and calculate the customers purchase
x = item - 1
price = menu[x][2]
prod = menu[x][1]

total = "{:.2f}".format((price * qty))

# lets start wrapping this up
print(f'\nOk, {name} your {str(qty)} "{prod}" will be ready in a few moments.\nYour total will be ${str(total)}.')
print("\nYou may pickup your order from the human at the next window.")

sys.exit(f"\nHave a nice {day_type} {name}!\n")
