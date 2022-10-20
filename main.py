"""This module is where the game 'loop' will run."""

import functions

functions.startmenu(functions.currentlng)
functions.player_quer()
functions.random_goal_gen(functions.numofgoals)

# 'ere be dragons.
while True:
    functions.hintcreation()
    functions.turncounter += 1
    if functions.turncounter % 2 == 0:
        functions.nextgoalturn()
        functions.hintcreation()
    functions.nextturn()
    functions.print_currentplayer_turn(functions.currentlng)
    functions.player_options_menu(functions.currentlng)
    functions.goalcheck(functions.currentplayer)
    functions.gameover()
    if functions.gameover():
        functions.scorecalc()
        functions.scoredisplay()
        functions.savescores()