"""This module contains most of the functions and variables needed to operate the game."""
# Required packages, mysql-connector-python, geopy

import random
import math
import time
import mysql.connector
import geopy.distance
import datetime

def cursor(inp):
    cursor = sqlconnect.cursor()
    cursor.execute(inp)


def cursor_fetchall(inp):
    cursor = sqlconnect.cursor()
    cursor.execute(inp)
    outcome = cursor.fetchall()
    return outcome