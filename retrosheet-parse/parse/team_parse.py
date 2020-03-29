#!/usr/bin/env python3.7
import csv
import mysql.connector

import credentials

filepath = "/Users/slatterydonohoe/Downloads/teams.csv"


# Class to parse team data from Retrosheet data files
# Description of files: https://www.retrosheet.org/team_codes.html
class TeamParse:
    cnx = mysql.connector.connect(user=credentials.sql['user'],
                                  password=credentials.sql['password'],
                                  database='mlb',
                                  auth_plugin='mysql_native_password')

    @staticmethod
    def send_team_to_db(int_id, team_id):
        cursor = TeamParse.cnx.cursor()
        try:
            cursor.callproc('add_team', [int_id, team_id, ])
        except mysql.connector.Error as error:
            print("Failed to execute stored procedure: {}".format(error))

    @staticmethod
    def parse_file(file):
        with open(file) as season_file:
            season_reader = csv.reader(season_file, delimiter=',')
            idx = 0
            for row in season_reader:
                TeamParse.send_team_to_db(idx, row[0])
                idx += 1


if __name__ == '__main__':
    TeamParse.parse_file(filepath)
    TeamParse.cnx.close()
