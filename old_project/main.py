"""This module is where the game 'loop' will run."""

import SQLfunctions

SQLfunctions.startmenu(SQLfunctions.lng_state)
SQLfunctions.plyr_quer()
SQLfunctions.random_goal_gen()

# 'ere be dragons.
while True:
    SQLfunctions.hintcreation()
    SQLfunctions.turncounter += 1
    if SQLfunctions.turncounter % 2 == 0:
        SQLfunctions.nextgoalturn()
        SQLfunctions.hintcreation()
    SQLfunctions.nextturn()
    SQLfunctions.print_currentplayer_turn(SQLfunctions.lng_state)
    SQLfunctions.player_options_menu(SQLfunctions.lng_state)
    SQLfunctions.goalcheck(SQLfunctions.currentplayer)
    SQLfunctions.gameover()
    if SQLfunctions.gameover() == True:
        SQLfunctions.scorecalc()
        SQLfunctions.scoredisplay()
        SQLfunctions.savescores()