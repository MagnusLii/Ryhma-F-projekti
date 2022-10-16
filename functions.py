"""This module contains most of the functions and variables needed to operate the game."""
# Required packages, mysql-connector-python, geopy

# Imports
import functions
import connection
import random
import math
import time
import geopy.distance
import datetime

# Vars
currentlng = 1  # 1 = English,
playercount = 1  # Number of players.
numofgoals = 4


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


def cursor(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)


def cursor_fetchall(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)
    outcome = sqlcursor.fetchall()
    return outcome


def startmenu(lng):
    if lng == 1:
        startmenuoption = ""
        while True:
            print("\n")
            print("[1]New game")
            print("[2]Options")
            print("[3]Credits")
            print("[4]Scoreboard")
            print("[0]Quit")
            try:
                startmenuoption = int(input(f"{BColors.OKCYAN}Enter choice: {BColors.ENDC}"))
            except ValueError:
                print(f"{BColors.CRED2}ERROR!\nInput int from available options.")
            if startmenuoption == 1:
                spacing()
                print(f"{BColors.CGREYBG}option 1{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                new_game(lng)
                return
            elif startmenuoption == 2:
                spacing()
                print(f"{BColors.CGREYBG}option 2{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                options(lng)
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")  # TODO create options.
                if startmenuoption == "":
                    continue
            elif startmenuoption == 3:
                spacing()
                print(f"{BColors.CGREYBG}option 3{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                gamecredits(lng)
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")
                if startmenuoption == "":
                    continue
            elif startmenuoption == 4:
                spacing()
                print(f"{BColors.CGREYBG}option 4{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                scoreboarddisplay()
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")
                if startmenuoption == "":
                    continue
            elif startmenuoption == 0:
                print(f"{BColors.OKCYAN}pwease down't weave me :(")
                exit()


def spacing():
    print("\n")


def options(lng):  # TODO add actual language select options
    if lng == 1:
        print("\n")
        print("[1]Language")


def gamecredits(lng):  # TODO Redo credits based on these instructions https://www.studiobinder.com/blog/where-credit-is-due-film-credits-order-hierarchy-with-free-film-credits-template/
    if lng == 1:
        print("\n")
        print("Made by:\n"
              "Misto #1 \n"
              "Magnus \n"
              "Jasper \n"
              "Daniel")


def scoreboarddisplay():
    query = f'''SELECT name, score
                FROM leaderboard
                ORDER BY score DESC
                FETCH FIRST 10 ROWS ONLY
                ;'''
    results = cursor_fetchall(query)
    placement = 1
    print(f"{BColors.OKCYAN}Current leaderboard top 10 players.{BColors.ENDC}")
    for row in results:
        print(f"[{placement}]Playername: [{row[0]}]          Score: [{row[1]}] points.")
        placement += 1


def new_game(lng):
    clear_data()
    if lng == 1:
        print("[1]Singleplayer\n"
              "[2]Multiplayer")
        while True:  # Determines number of players from user input.
            try:
                userchoice = int(input(f"{BColors.OKCYAN}#: {BColors.ENDC}"))
                if userchoice == 1:
                    functions.playercount = 1
                    spacing()
                    break
                elif userchoice == 2:
                    try:
                        functions.playercount = int(input(f"{BColors.OKCYAN}Input number of players: {BColors.ENDC}"))
                        spacing()
                        break
                    except ValueError:
                        print(f"{BColors.CRED2}Please only input numbers.{BColors.ENDC}")
                        spacing()
            except ValueError:
                print(f"{BColors.CRED2}Enter only from specified integer numbers.{BColors.ENDC}")
                spacing()
        player_setup(lng, playercount)


def clear_data():
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)


def player_setup(lng, numplayers):
    i = 1
    if lng == 1:
        while i <= numplayers:  # Creates players into database from userinput.
            playername = input(f"{BColors.OKCYAN}Enter {i} players name: {BColors.ENDC}")
            startinglocation = input("Enter chosen starting location\n"
                                     "or leave empty for default.\n"
                                     f"{BColors.OKCYAN}#: {BColors.ENDC}").upper()
            if startinglocation == "":
                startinglocation = "EGCC"
                spacing()
            status = check_icao(startinglocation)
            if status:
                query = f'''INSERT INTO game(id, co2_consumed, co2_budget, screen_name, location)
                        VALUES({i}, 0, 10000, "{playername}", "{startinglocation}")
                        ;'''
                cursor(query)
                i += 1
            elif not status:
                print(f"{BColors.CRED2}Error! ICAO not found in database list.{BColors.ENDC}")
                spacing()


def player_quer():
    query = f'''SELECT game.screen_name, game.location, game.co2_consumed
                FROM game
                GROUP BY game.id ASC
                ;'''
    templist = cursor_fetchall(query)
    for row in templist:
        print(f"Username: {row[0]}, "
              f"current location: {row[1]}, "
              f"co2 consumed: {row[2]}, ")
    spacing()


def random_goal_gen(goalnum):
    cursor("DELETE FROM goal;")
    tracknum = 1
    if tracknum > goalnum:
        return
    for i in range(goalnum):
        airportid = random.randint(1, 70942)  # Randomly selects a goal ID.
        query = f'''SELECT type, id FROM airport  
                        WHERE id = {airportid}
                        ;'''
        result = cursor_fetchall(query)
        for row in result:
            if row[0] == "closed":
                print(f"{BColors.CRED2}Closed airport in random_goal_gen func.{BColors.ENDC}")
                random_goal_gen(goalnum)
        query2 = f'''INSERT INTO goal (id, airportid)
                    VALUES({tracknum}, {airportid})
                    ;'''
        cursor(query2)
        print(f"ID = {tracknum}, airportid = {airportid}")
        tracknum += 1