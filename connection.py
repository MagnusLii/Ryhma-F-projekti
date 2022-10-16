import mysql.connector

sqlconnect = mysql.connector.connect(
    host="localhost",
    port="3306",
    database="flight_game",
    user="root",
    password="5579",
    autocommit=True
)
