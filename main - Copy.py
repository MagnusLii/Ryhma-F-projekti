"""This module is where the game 'loop' will run."""

import functions

functions.startmenu(functions.currentlng)
functions.player_quer()
functions.random_goal_gen(functions.numofgoals)
functions.hintcreation()

# 'ere be dragons.
while True:
    functions.turncounter += 1
    if functions.turncounter % 5 == 0:
        functions.nextgoalturn()
        functions.hintcreation()
    functions.nextturn()  # First turn will always be player 1 as their start time is always first.
    functions.kmfromgoal()
    functions.print_currentplayer_turn(functions.currentlng)
    functions.player_options_menu(functions.currentlng)
    functions.goalcheck(functions.currentplayer)
    functions.gameover()
    if functions.gameover():
        functions.scorecalc()
        functions.scoredisplay()
        functions.savescores()