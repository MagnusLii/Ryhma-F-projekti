"""This module contains most of the functions and variables needed to operate the game."""
# Required packages, mysql-connector-python, geopy

# Imports
import connection
import random
import math
import time
import mysql.connector
import geopy.distance
import datetime

# Vars
currentlng = 1

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'


def cursor(inp):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(inp)


def cursor_fetchall(inp):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(inp)
    outcome = sqlcursor.fetchall()
    return outcome

def startmenu(currentlng):
    if currentlng == 1:
        startmenuoption = 8
        while True:
            menu(currentlng)
            try:
                startmenuoption = int(input("Enter choice: "))
            except ValueError:
                print(f"{BColors.CRED2}Input int from available options.")
            if startmenuoption == 1:
                spacing()
                new_game(currentlng)
                return
            elif startmenuoption == 2:
                options(currentlng)
                nappi = "bruh"
                nappi = input("Press enter to go back")
                if nappi == "":
                    startmenuoption = 9
                    continue
            elif startmenuoption == 3:
                gamecredits(currentlng)
                nappi = "bruh"
                nappi = input("Press enter to go back")
                if nappi == "":
                    startmenuoption = 9
                    continue
            elif startmenuoption == 4:
                scoreboarddisplay()
                nappi = "bruh"
                nappi = input("Press enter to go back")
                if nappi == "":
                    startmenuoption = 9
                    continue
            elif startmenuoption == 0:
                break
            elif startmenuoption != 1 or startmenuoption != 2 or startmenuoption != 3:
                print("\n")
                print("\n")
                print(f"{BColors.CVIOLET2}INVALID INPUT{BColors.ENDC}")
                time.sleep(1)
                continue

def menu(currentlng):
    if currentlng == 1:
        print("\n")
        print("[1]New game")
        print("[2]Options")
        print("[3]Credits")
        print("[4]Scoreboard")
        print("[0]Quit")

startmenu(1)