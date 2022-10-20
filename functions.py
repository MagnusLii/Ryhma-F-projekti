"""This module contains most of the functions and variables needed to operate the game."""
# Required packages, mysql-connector-python, geopy

# TODO replace all "SQLfunctions" with "functions".
# TODO replace all "lngstate" with "currentlng".

# Imports
import functions
import connection
import random
import math
import time
import geopy.distance
import datetime  # Required! Handles datetime format in/from queries.

# Vars
currentlng = 1  # 1 = English,
playercount = 2  # Number of players.
numofgoals = 4  # Total number of goals generated in game.
goalturntracker = 0
activegoal = 1  # For keeping track of the latest player goal. Input from latestgoallookup()
currentplayer = 1
turncounter = 0  # Tracks in game turn, aka total turns.

# Lists
hintsround0 = ["", "", "", ""]    # For remembering hints generated by hintcreation() func.
hintsround1 = ["", "", "", ""]    # etc etc...
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


def startmenu(lng):
    if lng == 1:
        startmenuoption = ""
        while True:
            print("\n")  # TODO New colour for these kinds of lists potentially.
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
                #spacing()
                print(f"{BColors.CGREYBG}option 1{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                new_game(lng)
                return
            elif startmenuoption == 2:
                #spacing()
                print(f"{BColors.CGREYBG}option 2{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                options(lng)
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")  # TODO create options.
                if startmenuoption == "":
                    continue
            elif startmenuoption == 3:
                #spacing()
                print(f"{BColors.CGREYBG}option 3{BColors.ENDC}")  # TODO Remove before publish, troubleshooting only.
                gamecredits(lng)
                startmenuoption = input(f"{BColors.OKCYAN}Press enter to go back. {BColors.ENDC}")
                if startmenuoption == "":
                    continue
            elif startmenuoption == 4:
                #spacing()
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
                    #spacing()
                    break
                elif userchoice == 2:
                    try:
                        functions.playercount = int(input(f"{BColors.OKCYAN}Input number of players: {BColors.ENDC}"))
                        #spacing()
                        break
                    except ValueError:
                        print(f"{BColors.CRED2}Please only input numbers.{BColors.ENDC}")
                        #spacing()
            except ValueError:
                print(f"{BColors.CRED2}Enter only from specified integer numbers.{BColors.ENDC}")
                #spacing()
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
                #spacing()
            status = check_icao(startinglocation)
            if status:
                query = f'''INSERT INTO game(id, co2_consumed, co2_budget, screen_name, location)
                        VALUES({i}, 0, 10000, "{playername}", "{startinglocation}")
                        ;'''
                cursor(query)
                i += 1
            elif not status:
                print(f"{BColors.CRED2}Error! ICAO not found in database list.{BColors.ENDC}")
                #spacing()


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
    #spacing()


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
                    VALUES({i+1}, {airportid})
                    ;'''
        cursor(query2)


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


def nextgoalturn():
    if functions.goalturntracker > 3:
        return
    else:
        functions.goalturntracker += 1


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


def print_currentplayer_turn(lng):
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


def player_options_menu(lng):
    if lng == 1:
        while True:
            print("Choose what you wish to do.\n"  # TODO New colour for these kinds of lists potentially.
                  '[1] Lookup ICAO code.\n'
                  '[2] Move to new airport.\n'
                  '[3] Look at current player information.\n'
                  '[4] List hints.')
            playerchoice = input(f"{BColors.OKCYAN}#: {BColors.ENDC}")
            #spacing()
            if playerchoice == "1":
                findicao(currentlng)
            if playerchoice == "2":
                relocate(currentlng)
                return
            if playerchoice == "3":
                player_quer()
            if playerchoice == "4":
                printallhints()


def findicao(lng):
    if lng == 1:
        print("Select which filters you wish to use.\n"  # TODO New colour for these kinds of lists potentially.
              '[1] for airportname.\n'
              '[2] for airporttype.\n'
              '[3] for continent.\n'
              '[4] for country ISO code.\n'
              '[5] for Country region iso code\n'
              '[6] for municipality name\n'
              '"Exit" to exit search.')
        filterselect = input("Input chosen filters: ").upper()  # TODO Add additional valueerror handling.
        #spacing()
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
        for row in results:
            print(f'{BColors.CYELLOW}"Name":{BColors.ENDC} {row[0]}, '
                  f'{BColors.CYELLOW}"Type":{BColors.ENDC} {row[1]}, '
                  f'{BColors.CYELLOW}"Continent":{BColors.ENDC} {row[2]}, '
                  f'{BColors.CYELLOW}"Country":{BColors.ENDC} {row[3]}, '
                  f'{BColors.CYELLOW}"RegionISO":{BColors.ENDC} {row[5]}, '
                  f'{BColors.CYELLOW}"Municipality":{BColors.ENDC} {row[6]}, '
                  f'{BColors.CYELLOW}"ICAO":{BColors.ENDC} {row[4]}.')
        return


def relocate(lng):
    if lng == 1:
        print("Which terminal do you wish to travel to?\n"
              '"Input" its ICAO code.')
        while True:
            newlocation = input(f"{BColors.OKCYAN}#: {BColors.ENDC}").upper()
            if check_icao(newlocation):
                co2perkm = list_available_aircraft(lng, movement_calc_km(newlocation),
                                                   aircraft_availability_detect(
                                                       currentplayer_currentloc(lng),
                                                       newlocation))
                distance = movement_calc_km(newlocation)
                updateco2(currentplayer, movement_calc_co2(distance, co2perkm))
                moveplayer(newlocation, currentplayer, aircraftid_fromco2(co2perkm))
                print(f"{BColors.CYELLOW}You are moving to your destination.{BColors.ENDC}")
                #spacing()
                return
            else:
                print(f"{BColors.CRED2}ICAO not found in terminal database. Please try again.{BColors.ENDC}")
                #spacing()


def movement_calc_km(endloc):
    query = f'''SELECT game.location FROM game
                WHERE game.id = "{currentplayer}"
                ;'''
    distancekm = str(geopy.distance.geodesic(getcoords(cursor_fetchall(query)), getcoords(endloc)))
    distancekm = distancekm[:8]
    distancekm = float(distancekm)  # Required, conversion into INT often won't work otherwise.
    return int(distancekm)


def getcoords(icao):
    query = f'''SELECT latitude_deg, longitude_deg 
        FROM airport WHERE ident = "{icao}"'''
    return cursor_fetchall(query)


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


def list_available_aircraft(lng, distancekm, aircrafttypenum):
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
        return confirm_aircrafttype(lng, aircraft)


def updateco2(playerid, co2toadd):
    query = f'''UPDATE game
            SET co2_consumed = co2_consumed + {co2toadd}
            WHERE id = "{playerid}"
            ;'''
    cursor(query)


def movement_calc_co2(distance, co2perkm):
    return distance * co2perkm



def confirm_aircrafttype(lng, aircrafttuple):
    if lng == 1:
        chosenaircraft = None
        while chosenaircraft is None:
            try:
                chosenaircraft = int(input("Choose aircraft: "))
                for row in aircrafttuple:
                    if chosenaircraft == int(row[0]):
                        return int(row[3])  # returns amount of Co2 per KM of chosen aircraft.
                print(f"{BColors.CRED2}Input integer from available options.\n{BColors.ENDC}")
                confirm_aircrafttype(1, aircrafttuple)
            except ValueError:
                print(f"{BColors.CRED2}Input integer!{BColors.ENDC}")


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


def updatenextturn(playerid, mintoadd):
    query = f'''UPDATE game
            SET next_turn = next_turn + INTERVAL {mintoadd} MINUTE
            WHERE id = "{playerid}"
            ;'''
    cursor(query)
    return


def aircraftid_fromco2(co2usage):
    query = f'''SELECT lentoalukset.id
            FROM lentoalukset
            WHERE lentoalukset.co2_per_km = {co2usage}'''
    acid = str(cursor_fetchall(query))
    delthese = "[()],.'¨"
    for char in delthese:
        acid = acid.replace(char, "")
    return int(acid)


def printallhints():
    for row in hintsall[currentgoalid()]:
        if row != "":
            print(row)


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
            endscore = (math.sqrt((co2 - (420 * (times ** 2))/69) ** 2)) / 42069  # TODO redoscore calc WTF?!?!??!!!!!
            endscore = round(endscore)
            endscore = int(endscore)
            endscores.append(endscore)
        trackingnum += 1


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