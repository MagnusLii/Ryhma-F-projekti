"""This module contains most of the functions and variables needed to operate the game."""
# Required packages, mysql-connector-python, geopy

# Imports
import functions  # Required, used in functions with complex scopes that don't handle global vars properly.
import connection
import random
import math
import geopy.distance
import datetime  # Required! Handles datetime format in/from queries.
global questions  # Used in sidequests, DO NOT USE ELSEWHERE!
global original_questions_list  # Used in sidequests, DO NOT USE ELSEWHERE!

# Vars
currentlng = 1  # 1 = English,
playercount = 2  # Number of players.
numofgoals = 4  # Total number of goals generated in game.
goalturntracker = 0
activegoal = 1  # For keeping track of the latest player goal. Input from latestgoallookup()
currentplayer = 1
turncounter = 0  # Tracks in game turn, aka total turns.

# Lists
hintsround0 = ["", "", "", ""]  # For remembering hints generated by hintcreation() func.
hintsround1 = ["", "", "", ""]  # etc etc...
hintsround2 = ["", "", "", ""]
hintsround3 = ["", "", "", ""]
hintsall = [hintsround0, hintsround1, hintsround2, hintsround3]
endscores = []


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


# Creates a menu for the player from which they choose what they wish to do.
def startmenu(lng):
    if lng == 1:
        startmenuoption = ""
        while True:
            # TODO New colour for these kinds of lists potentially.
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
                new_game(lng)
                return
            elif startmenuoption == 2:
                options(lng)
                startmenuoption = input(
                    f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")  # TODO create options.
                if startmenuoption == "":
                    continue
            elif startmenuoption == 3:
                gamecredits(lng)
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")
                if startmenuoption == "":
                    continue
            elif startmenuoption == 4:
                scoreboarddisplay()
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")
                if startmenuoption == "":
                    continue
            elif startmenuoption == 0:
                print(f"{BColors.OKCYAN}pwease down't weave me :(")
                exit()


# Lists available options.
def options(lng):  # TODO add actual language select options
    if lng == 1:
        print("[1]Language")


# Lists credits.
def gamecredits(
        lng):  # TODO Redo credits based on these instructions https://www.studiobinder.com/blog/where-credit-is-due-film-credits-order-hierarchy-with-free-film-credits-template/
    if lng == 1:
        print("Made by:\n"
              "Misto #1 \n"
              "Magnus \n"
              "Jasper \n"
              "Daniel")


# Displays top 10 highest scoring players (and scores) of all time.
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


# Sets up a new game byt modifying the DB.
def new_game(lng):
    clear_data()
    if lng == 1:
        while True:  # Determines number of players from user input.
            print("[1]Singleplayer\n"
                  "[2]Multiplayer")
            try:
                userchoice = int(input(f"{BColors.OKCYAN}#: {BColors.ENDC}"))
                if userchoice == 1:
                    functions.playercount = 1
                    break
                elif userchoice == 2:
                    try:
                        functions.playercount = int(input(f"{BColors.OKCYAN}Input number of players: {BColors.ENDC}"))
                        break
                    except ValueError:
                        print(f"{BColors.CRED2}Please only input integer numbers.{BColors.ENDC}")
            except ValueError:
                print(f"{BColors.CRED2}Input numbers.{BColors.ENDC}")
            else:
                print(f"{BColors.CRED2}Enter only from specified numbers.{BColors.ENDC}")
        player_setup(lng, playercount)


# clears goal and game data from DB.
def clear_data():
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)


# Sets up the players for a game.
def player_setup(lng, numplayers):
    i = 1
    if lng == 1:
        while i <= numplayers:  # Creates players into database from userinput.
            playername = ""
            while playername == "":
                playername = input(f"{BColors.OKCYAN}Enter {i} players name: {BColors.ENDC}")
                if playername == "":
                    print(f"{BColors.CRED2}Input a name.{BColors.ENDC}")
            startinglocation = input("Enter chosen starting location\n"
                                     "or leave empty for default.\n"
                                     f"{BColors.OKCYAN}#: {BColors.ENDC}").upper()
            if startinglocation == "":
                startinglocation = "EGCC"
            status = check_icao(startinglocation)
            if status:
                query = f'''INSERT INTO game(id, screen_name, location)
                        VALUES({i}, "{playername}", "{startinglocation}")
                        ;'''
                cursor(query)
                i += 1
            elif not status:
                print(f"{BColors.CRED2}Error! ICAO not found in database list.{BColors.ENDC}")


# Queries and displays the current situation of all players
def player_quer():
    query = f'''SELECT game.screen_name, game.location, game.co2_consumed, game.next_turn, game.starttime
                FROM game
                GROUP BY game.id ASC
                ;'''
    templist = cursor_fetchall(query)
    for row in templist:
        timespent = row[3] - row[4]
        timespent = int(timespent.total_seconds()) / 3600
        print(f"{BColors.CYELLOW}Username:{BColors.ENDC} {row[0]}, "
              f"{BColors.CYELLOW}current location:{BColors.ENDC} {row[1]}, "
              f"{BColors.CYELLOW}co2 consumed:{BColors.ENDC} {row[2]}, "
              f"{BColors.CYELLOW}time spent:{BColors.ENDC} {timespent} hours.")


# Generates random goals for the game.
def random_goal_gen(goalnum):
    cursor("DELETE FROM goal;")
    for i in range(goalnum):
        airportid = random.randint(1, 70942)
        query = f'''SELECT type, id FROM airport  
                        WHERE id = {airportid}
                        ;'''
        result = cursor_fetchall(query)
        for row in result:
            if row[0] == "closed":
                random_goal_gen(goalnum)
                return
        query2 = f'''INSERT INTO goal (id, airportid)
                    VALUES({i + 1}, {airportid})
                    ;'''
        cursor(query2)


# Verifies if a specified ICAO code is valid.
def check_icao(icaocode):
    query = f'''SELECT ident FROM airport
                WHERE ident = "{icaocode}"
                ;'''
    result = cursor_fetchall(query)
    for row in result:
        if row[0] == "closed":
            print(f"{BColors.CRED2}Error\n{BColors.ENDC}"
                  f"{BColors.CRED2}The specified airport is currently closed. {BColors.ENDC}")
            return False
    if len(result) == 0:  # True means specified ICAO was found, False means incorrect ICAO.
        return False
    else:
        return True


# Creates hints for the goal the current player is after.
def hintcreation():
    if goalturntracker == 0:
        query = f'''SELECT airport.continent, airport.type
                    FROM airport, goal
                    WHERE goal.id = {functions.activegoal}
                    AND airport.id = goal.airportid
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            hint = f'{BColors.CYELLOW}The airport is of the type "{row[1]}",' \
                   f' and is located on the "{row[0]}" continent.{BColors.ENDC}'
            if hintsall[currentgoalid()][0] == "":
                hintsall[currentgoalid()][0] = hint
                print(hint)
            else:
                print(hintsall[currentgoalid()][0])
    elif goalturntracker == 1:
        query = f'''SELECT airport.iso_country, country.name
                    FROM airport, goal, country
                    WHERE goal.id = {functions.activegoal}
                    AND airport.iso_country = country.iso_country
                    AND airport.id = goal.airportid
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            hint = f'{BColors.CYELLOW}The airport is located in the country of [{row[0]}]: {row[1]}.{BColors.ENDC}'
            if hintsall[currentgoalid()][1] == "":
                hintsall[currentgoalid()][1] = hint
                print(hint)
            else:
                print(hintsall[currentgoalid()][1])
    elif goalturntracker == 2:
        query = f'''SELECT airport.iso_region, airport.iso_country, country.name
                    FROM airport, goal, country
                    WHERE goal.id = {functions.activegoal}
                    AND airport.iso_country = country.iso_country
                    AND airport.id = goal.airportid
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            hint = f'{BColors.CYELLOW}The airport is located region of [{row[0]}]' \
                   f' within the country of [{row[1]}]: {row[2]}.{BColors.ENDC}'
            if hintsall[currentgoalid()][2] == "":
                hintsall[currentgoalid()][2] = hint
                print(hint)
            else:
                print(hintsall[currentgoalid()][2])
    elif goalturntracker == 3:
        query = f'''SELECT airport.municipality, airport.iso_country, country.name
                    FROM airport, goal, country
                    WHERE goal.id = {functions.activegoal}
                    AND airport.iso_country = country.iso_country
                    AND airport.id = goal.airportid
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            hint = f'{BColors.CYELLOW}The airport is located within the municipality of [{row[0]}],' \
                   f' within the country of [{row[1]}]: {row[2]}.{BColors.ENDC}'
            if hintsall[currentgoalid()][3] == "":
                hintsall[currentgoalid()][3] = hint
                print(hint)
            else:
                print(hintsall[currentgoalid()][3])
    else:
        print(f"{BColors.CRED2}ERROR\n goalturntracker var out of bounds in hintcreation func{BColors.ENDC}")


# Returns ID of current target goal.
def currentgoalid():
    query = f'''SELECT goal_reached.goal_id
                FROM goal_reached
                WHERE goal_reached.game_id = {currentplayer}
                ORDER BY goal_reached.goal_id DESC
                FETCH FIRST 1 ROWS ONLY
                ;'''
    result = cursor_fetchall(query)
    if not result:
        return 0
    else:
        for j in result:
            string = str(j)
            delthese = "[()],.'¨"
            for char in delthese:
                string = string.replace(char, "")
            # goalID index starts from 1 in db, 0 in pyth lists.
            return int(string) - 1


# updates goalturntracker var.
def nextgoalturn():
    if functions.goalturntracker > 3:
        return
    else:
        functions.goalturntracker += 1


# Checks who's turn it is next and updates currentplayer var accordingly.
def nextturn():
    keeptracknum = 0
    nextupcoming = 0
    dtimelist = []
    query = f'''SELECT id, next_turn FROM game
            ;'''
    alldates = cursor_fetchall(query)
    for row in alldates:
        dtime = row[1]
        dtimelist.append(dtime)
        if dtimelist[keeptracknum] <= dtimelist[nextupcoming]:
            nextupcoming = keeptracknum
        keeptracknum += 1
    functions.currentplayer = nextupcoming + 1


# prints who's turn it is.
def print_currentplayer_turn(lng=currentlng):
    if lng == 1:
        query = f'''SELECT screen_name
                FROM game
                WHERE id = {currentplayer}'''
        result = cursor_fetchall(query)
        name = str(result[0])
        delthese = "[()],.'¨"
        for char in delthese:
            name = name.replace(char, "")
        print(f"{BColors.CYELLOW}It is now {name}'s turn.{BColors.ENDC}")


# creates a menu of choices for the player to navigate in game.
def player_options_menu(lng=currentlng):
    validinputs = ["1", "2", "3", "4", "5", "6", "EXIT"]
    validinputdetected = False
    if lng == 1:
        while True:
            print("Choose what you wish to do.\n"  # TODO New colour for these kinds of lists potentially.
                  '[1] Lookup ICAO code.\n'
                  '[2] Move to new airport.\n'
                  '[3] Look at current player information.\n'
                  '[4] List hints.')
            playerchoice = input(f"{BColors.OKCYAN}#: {BColors.ENDC}")
            for char in playerchoice:
                if char in validinputs:
                    validinputdetected = True
            if not validinputdetected:
                print(f"{BColors.CRED2}No valid inputs detected!{BColors.ENDC}")
                continue
            if playerchoice == "1":
                findicao(currentlng)
            if playerchoice == "2":
                if relocate(currentlng):
                    continue
                else:
                    return
            if playerchoice == "3":
                player_quer()
            if playerchoice == "4":
                printallhints()


# Filtering system used by players to lookup ICAO codes.
def findicao(lng=currentlng):
    validinputs = ["1", "2", "3", "4", "5", "6", "EXIT"]
    validinputdetected = False
    if lng == 1:
        print("Select which filters you wish to use.\n"  # TODO New colour for these kinds of lists potentially.
              '[1] for airportname.\n'
              '[2] for airporttype.\n'
              '[3] for continent.\n'
              '[4] for country ISO code.\n'
              '[5] for Country region iso code\n'
              '[6] for municipality name\n'
              '["Exit"] to exit search.')
        filterselect = input("Input chosen filters: ").upper()
        for char in filterselect:
            if char in validinputs:
                validinputdetected = True
            elif filterselect in validinputs:
                validinputdetected = True
        if not validinputdetected:
            print(f"{BColors.CRED2}No valid inputs detected!{BColors.ENDC}")
            return
        airportname = ""
        airporttype = ""
        airportcontinent = ""
        countryname = ""
        regioniso = ""
        municipality = ""
        if "EXIT" in filterselect:
            return
        if "1" in filterselect:
            airportname = input(f"{BColors.OKCYAN}Input airportname filter: {BColors.ENDC}")
        if "2" in filterselect:
            airporttype = input(f"{BColors.OKCYAN}Input airporttype filter: {BColors.ENDC}")
        if "3" in filterselect:
            airportcontinent = input(f"{BColors.OKCYAN}Input Continent ISO code (EU, OC, AF...): {BColors.ENDC}")
        if "4" in filterselect:
            countryname = input(f"{BColors.OKCYAN}Input country name: {BColors.ENDC}")
        if "5" in filterselect:
            regioniso = input(f"{BColors.OKCYAN}Input country region ISO code: {BColors.ENDC}")
        if "6" in filterselect:
            municipality = input(f"{BColors.OKCYAN}Input municipality name: {BColors.ENDC}")
        query = f'''SELECT airport.name, airport.type, airport.continent,
                country.name, airport.ident, airport.iso_country, airport.municipality
                FROM airport, country
                WHERE country.iso_country = airport.iso_country
                AND airport.name LIKE "%{airportname}%"
                AND airport.type LIKE "%{airporttype}%"
                AND airport.continent LIKE "%{airportcontinent}%"
                AND country.name LIKE "%{countryname}%"
                AND airport.iso_country LIKE "%{regioniso}%"
                AND airport.municipality LIKE "%{municipality}%"
                ORDER BY airport.name ASC
                ;'''
        results = cursor_fetchall(query)
        if not results:
            print(f"{BColors.CYELLOW}No matching results found.{BColors.ENDC}")
        for row in results:
            print(f'{BColors.CYELLOW}"Name":{BColors.ENDC} {row[0]}, '
                  f'{BColors.CYELLOW}"Type":{BColors.ENDC} {row[1]}, '
                  f'{BColors.CYELLOW}"Continent":{BColors.ENDC} {row[2]}, '
                  f'{BColors.CYELLOW}"Country":{BColors.ENDC} {row[3]}, '
                  f'{BColors.CYELLOW}"RegionISO":{BColors.ENDC} {row[5]}, '
                  f'{BColors.CYELLOW}"Municipality":{BColors.ENDC} {row[6]}, '
                  f'{BColors.CYELLOW}"ICAO":{BColors.ENDC} {row[4]}.')
        return


# Moves player to their chosen destination and updates time and co2 accordingly.
def relocate(lng=currentlng):
    if lng == 1:
        while True:
            co2perkm = None
            if co2perkm == 42069:
                return True
            print("Which terminal do you wish to travel to?\n"
                  '"Input" its ICAO code.')
            newlocation = input(f"{BColors.OKCYAN}#: {BColors.ENDC}").upper()
            if check_icao(newlocation):
                co2perkm = list_available_aircraft(movement_calc_km(newlocation),
                                                   aircraft_availability_detect(
                                                       currentplayer_currentloc(lng),
                                                       newlocation))
                if co2perkm == 42069:  # Only true if player chose to exit the functions that return a proper value
                    # before proper assignment
                    return True
                distance = movement_calc_km(newlocation)
                updateco2(currentplayer, movement_calc_co2(distance, co2perkm))
                moveplayer(newlocation, currentplayer, aircraftid_fromco2(co2perkm))
                randomnum = random.randint(1, 6)
                if randomnum >= 4:
                    side_quest()
                print(f"{BColors.CYELLOW}You are moving to your destination.{BColors.ENDC}")
                return
            else:
                print(f"{BColors.CRED2}ICAO not found in terminal database. Please try again.{BColors.ENDC}")


# calculates distance between the players current location and destination.
def movement_calc_km(endloc):
    query = f'''SELECT game.location FROM game
                WHERE game.id = "{currentplayer}"
                ;'''
    distancekm = str(geopy.distance.geodesic(getcoords(cursor_fetchall(query)), getcoords(endloc)))
    distancekm = distancekm[:8]
    distancekm = float(distancekm)  # Required, conversion into INT often won't work otherwise.
    return int(distancekm)


# Queries long and lat coords from DB based on ICAO.
def getcoords(icao):
    query = f'''SELECT latitude_deg, longitude_deg 
        FROM airport WHERE ident = "{icao}"'''
    return cursor_fetchall(query)


# Fetches current players current location.
def currentplayer_currentloc(currentplayerid):
    query = f'''SELECT location FROM game
            WHERE id = "{currentplayerid}"
            ;'''
    result = cursor_fetchall(query)

    icao = str(result[0])
    delthese = "[()],.'¨"
    for char in delthese:
        icao = icao.replace(char, "")
    return icao


# Filters aircraft types based on players starting and end location.
def aircraft_availability_detect(startloc, endloc):
    availableaircrafttype = [1, 2, 3, 4, 5]
    airporttypes = []
    startlocquery = f'''SELECT type FROM airport
                    WHERE ident = "{startloc}"
                    ;'''
    endlocquery = f'''SELECT type FROM airport
                    WHERE ident = "{endloc}"
                    ;'''
    airporttypes.append(cursor_fetchall(startlocquery))
    airporttypes.append(cursor_fetchall(endlocquery))

    trackingnum = 0
    for j in airporttypes:
        name = str(j)
        delthese = "[()],.'¨"
        for char in delthese:
            name = name.replace(char, "")
        airporttypes[trackingnum] = name
        trackingnum += 1

    for i in airporttypes:
        if i == "balloonport":
            unwanted_num = {4, 3, 1, 5}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "closed":
            print(f"{BColors.CRED2}The airport you attempted to move to is closed\n{BColors.ENDC}"
                  f"{BColors.CRED2}Please select an open airport.{BColors.ENDC}")
            player_options_menu(currentlng)
            unwanted_num = {4, 3, 2, 1, 5}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "heliport":
            unwanted_num = {4, 1, 5}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "large_airport":
            unwanted_num = {4}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "medium_airport":
            unwanted_num = {4}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "small_airport":
            unwanted_num = {4, 5}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        elif i == "seaplane_base":
            unwanted_num = {1, 5}
            availableaircrafttype = [ele for ele in availableaircrafttype if ele not in unwanted_num]
        if not availableaircrafttype:
            print(f"{BColors.CRED2}There are no aircraft capable of moving between selected airports.\n{BColors.ENDC}"
                  f"{BColors.CRED2}Please choose another location.{BColors.ENDC}")
            player_options_menu(currentlng)
    return availableaircrafttype


# creates a list for the player of aircraft they are able to use for their flight.
def list_available_aircraft(distancekm, aircrafttypenum, lng=currentlng):
    trackingnum = 0
    if lng == 1:
        if len(aircrafttypenum) == 1:
            aircrafttypes = str(aircrafttypenum[0])
        else:
            aircrafttypes = str(aircrafttypenum[0])
            for i in aircrafttypenum:
                aircrafttypes = f"{aircrafttypes} or type_numeric = {aircrafttypenum[trackingnum]}"
                trackingnum += 1

        matching_aircraftquer = f'''SELECT ROW_NUMBER() OVER() AS num_row, id, model_name, co2_per_km, speed_kmh
                                FROM lentoalukset
                                WHERE type_numeric = {aircrafttypes}
                                AND max_range_km > {distancekm}
                                ;'''
        aircraft = functions.cursor_fetchall(matching_aircraftquer)
        if not aircraft:
            print("There are no aircraft capable of making this journey, we suggest traveling to a closer airport.")
            player_options_menu(lng)
        print(f"{BColors.CYELLOW}Here are the compatible aircraft.{BColors.ENDC}")
        for row in aircraft:
            print(f"[{row[0]}]{row[2]}, co2 produced per KM: {row[3]}, Speed KM/h: {row[4]}.")
        print(f"[{len(aircraft) + 1}]Select to go back.")
        return confirm_aircrafttype(aircraft)


# Updates co2 used for the player.
def updateco2(playerid, co2toadd):
    query = f'''UPDATE game
            SET co2_consumed = co2_consumed + {co2toadd}
            WHERE id = "{playerid}"
            ;'''
    cursor(query)


# calculates co2 used on a journey.
def movement_calc_co2(distance, co2perkm):
    return distance * co2perkm


# Confirms what aircraft to use from player and returns the amount of co2 it uses perkm.
def confirm_aircrafttype(aircrafttuple, lng=currentlng):
    if lng == 1:
        chosenaircraft = None
        while chosenaircraft is None:
            try:
                chosenaircraft = int(input("Choose aircraft: "))
                for row in aircrafttuple:
                    if chosenaircraft == int(row[0]):
                        return int(row[3])  # returns amount of Co2 per KM of chosen aircraft.
                    elif chosenaircraft == int(len(aircrafttuple) + 1):
                        return 42069
                print(f"{BColors.CRED2}Input integer from available options.\n{BColors.ENDC}")
                confirm_aircrafttype(aircrafttuple)
            except ValueError:
                print(f"{BColors.CRED2}Input integer!{BColors.ENDC}")


# moves player to their chosen destination.
def moveplayer(endloc, playerid, acid):
    query = f'''UPDATE game
            SET location = "{endloc}"
            WHERE id = {playerid}
            ;'''
    if check_icao(endloc):
        cursor(query)
        updatenextturn(playerid, movement_calc_time(endloc, acid))
    else:
        print(f"{BColors.CVIOLET2}Error 'check_ICAO' not passed in 'moveplayer'{BColors.ENDC}")


# calculates time used for journey.
def movement_calc_time(endloc, aircraftid):
    query = f'''SELECT game.location FROM game
            WHERE game.id = "{currentplayer}"
            ;'''
    query2 = f'''SELECT lentoalukset.speed_kmh 
                FROM lentoalukset
                WHERE lentoalukset.id = "{aircraftid}"
                ;'''
    distancekm = str(geopy.distance.geodesic(getcoords(cursor_fetchall(query)), getcoords(endloc)))
    delthese = "km "
    for char in delthese:  # Removes " km" from end of geodesic str.
        distancekm = distancekm.replace(char, "")
    distancekm = float(distancekm)
    speed = str(cursor_fetchall(query2))
    delthese = "[()],.'¨"
    for char in delthese:
        speed = speed.replace(char, "")
    return round(int((distancekm // int(speed)) * 60))


# updates the time at which current player will have their next turn.
def updatenextturn(playerid, mintoadd):
    query = f'''UPDATE game
            SET next_turn = next_turn + INTERVAL {mintoadd} MINUTE
            WHERE id = "{playerid}"
            ;'''
    cursor(query)
    return


# determines and returns aircraft ID based on co2perkm usage.
def aircraftid_fromco2(co2usage):
    query = f'''SELECT lentoalukset.id
            FROM lentoalukset
            WHERE lentoalukset.co2_per_km = {co2usage}'''
    acid = str(cursor_fetchall(query))
    delthese = "[()],.'¨"
    for char in delthese:
        acid = acid.replace(char, "")
    return int(acid)


# prints all available hints for the goal current player is after.
def printallhints():
    for row in hintsall[currentgoalid()]:
        if row != "":
            print(row)


# determines if player has reached a goal and updates the info into DB.
def goalcheck(player):
    query = f'''SELECT airport.id
                FROM airport, game
                WHERE game.id = {player}
                AND game.location = airport.ident
                ;'''
    query2 = f'''SELECT airportid, id
                FROM goal
                ;'''
    currentlocid = cursor_fetchall(query)
    goalids = cursor_fetchall(query2)
    for j in currentlocid:
        temp = str(j)
        delthese = "[()],.'¨"
        for char in delthese:
            temp = temp.replace(char, "")
        currentlocid = temp
    for row in goalids:
        query3 = f'''INSERT INTO goal_reached(goal_id, game_id)
                    VALUES({row[1]}, {currentplayer})
                    ;'''
        if str(row[0]) == str(currentlocid):
            cursor(query3)
            query4 = f'''UPDATE goal
                        SET goalreached = 1
                        WHERE airportid = {currentlocid}
                        ;'''
            cursor(query4)  # sets goalreached flag into goals table.
            functions.goalturntracker = 0


# Checks if the game is over.
def gameover():
    playerid = 1
    for i in range(playercount):
        query = f'''SELECT goal_id
                        FROM goal_reached
                        WHERE game_id = {playerid}
                        ;'''
        result = cursor_fetchall(query)
        if len(result) == 4:
            playerid += 1
            continue
        else:
            return False
    return True


# Calculates scores
def scorecalc():
    trackingnum = 1
    for i in range(playercount):
        query = f'''SELECT game.co2_consumed, game.starttime, game.next_turn
                    FROM game
                    WHERE id = {trackingnum}
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            times = row[2] - row[1]
            times = int(times.total_seconds())
            co2 = int(row[0])
            endscore = (math.sqrt((co2 - (420 * (times ** 2)) / 69) ** 2)) / 42069  # TODO redoscore calc WTF?!?!??!!!!!
            endscore = round(endscore)
            endscore = int(endscore)
            endscores.append(endscore)
        trackingnum += 1


# prints every players end score.
def scoredisplay():
    trackingnum = 1
    for i in range(playercount):
        query = f'''SELECT screen_name
                    FROM game
                    WHERE id = {trackingnum}
                    ;'''
        result = cursor_fetchall(query)
        for row in result:
            print(f"{row[0]} earned {endscores[i]} points.")
        trackingnum += 1


# Saves all scores into DB.
def savescores():
    trackingnum = 1
    for i in range(playercount):
        query = f'''SELECT screen_name
                            FROM game
                            WHERE id = {trackingnum}
                            ;'''
        result = cursor_fetchall(query)
        for row in result:
            query2 = f'''INSERT INTO leaderboard(name, score)
                        VALUE("{row[0]}", {endscores[i]})'''
            cursor(query2)
        trackingnum += 1


# prints the distance between players current loc and their goal.
def kmfromgoal(player=currentplayer, currentgoal=currentgoalid()):
    currentcoords = cursor_fetchall(f'''SELECT airport.latitude_deg, airport.longitude_deg
                                    FROM airport, game
                                    WHERE game.id = {player}
                                    AND game.location = airport.ident
                                    ;''')
    airportid = str(cursor_fetchall(f'''SELECT goal.airportid
                                    FROM goal
                                    WHERE goal.id = {currentgoal + 1}
                                    ;'''))
    delthese = "[()],.'¨"
    for char in delthese:
        airportid = airportid.replace(char, "")
    goalcoords = cursor_fetchall(f'''SELECT airport.latitude_deg, airport.longitude_deg
                                 FROM airport
                                 WHERE id = {airportid}''')
    print(f'{BColors.CYELLOW}You are currently {geopy.distance.geodesic(currentcoords, goalcoords)} '
          f'from the goal.{BColors.ENDC}')


globals()["questions"] = [
        {"q": "k?", "a": "kkk"},
        {"q": "k2?", "a": "kkk2"},
        {"q": "k3?", "a": "kkk3"},
        {"q": "k4?", "a": "kkk4"},
        {"q": "k5?", "a": "kkk5"},
        {"q": "k6?", "a": "kkk6"}
    ]
globals()["original_questions_list"] = [
        {"q": "k?", "a": "kkk"},
        {"q": "k2?", "a": "kkk2"},
        {"q": "k3?", "a": "kkk3"},
        {"q": "k4?", "a": "kkk4"},
        {"q": "k5?", "a": "kkk5"},
        {"q": "k6?", "a": "kkk6"}
    ]


def side_quest():

    question_list_size = len(globals()["questions"])
    if question_list_size < 3:
        globals()["questions"] = globals()["original_questions_list"].copy()
    list_of_questions = [globals()["questions"].pop(random.randrange(len(globals()["questions"]))) for _ in range(random.randint(1, 3))]

    for i in list_of_questions:
        print(i["q"])
        answer = input(f"{BColors.OKCYAN}Answer Yes(y) or No(n): {BColors.ENDC}")
        if answer == i["a"]:
            print(f"{BColors.CYELLOW}Congratulations you earned 500 points.{BColors.ENDC}")
            addpointsquery = f'''UPDATE game
                              SET points = points + 500
                              WHERE id = {currentplayer}
                              ;'''
            cursor(addpointsquery)
        else:
            print(f"{BColors.CYELLOW}Wrong. :({BColors.ENDC}")
