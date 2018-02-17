#!/usr/bin/python3
""" Matchmaking tool for task one of "Wargaming Forge" """


import os
import linecache
import re

class Matchmaker:
    """ Gets directory, containing players.txt and teams.txt as a param"""

    def __init__(self, test_directory):
        self.available_teams = []
        self.team_number = 0
        self.test_directory = test_directory
        self.working_dir = os.path.join(os.path.abspath("."), self.test_directory)


    def populate_teams(self):
        """ Calculates quantity of teams in teams.txt and adds them to available_teams list"""

        with open(os.path.join(self.working_dir, "teams.txt")) as teams_file:
            for lines in teams_file:
                self.team_number += 1
        teams_file.close()
        for team_id in range(0, self.team_number):
            self.available_teams.append(self.get_team_rating(team_id))


    def sort_list(self):
        """ Sortes teams by rating """
        self.available_teams.sort()


    def rivals(self):
        """ Creates test_*.txt in corresponding working test dir and after that
            iterates through available_teams with step of two to add closest pairs of teams"""
        pairs_file = open(os.path.join(
            self.working_dir, "{}_pairs.txt".format(self.test_directory)), "w")
        if self.team_number % 2 == 0:
            for i in range(0, self.team_number, 2):
                pairs_file.writelines("{} {}\n".
                                      format(self.available_teams[i][1],
                                             self.available_teams[i + 1][1]))
        else:
            for i in range(0, (self.team_number - 2), 2):
                pairs_file.writelines("{} {}\n".
                                      format(self.available_teams[i][1],
                                             self.available_teams[i + 1][1]))
            pairs_file.writelines("{}\n".format(self.available_teams[self.team_number - 1][1]))
            pairs_file.close()

    def get_player_rating(self, player_id):
        """ Gets player id as a param and after it looks for rating of that player.
            Returns rating"""
        line = linecache.getline(os.path.join(self.working_dir, "players.txt"), player_id + 1)
        rating = int(line.split()[1])
        return rating


    def get_team_rating(self, team_id):
        """ Gets team id as a param then iterates through players in corresponding team in teams.txt
            calling get_player_rating.
            Returns list with team rating and team id"""
        team_rating = 0
        team = linecache.getline(os.path.join(self.working_dir, "teams.txt"), team_id + 1)
        for player in team.split()[1:]:
            player_rating = int(self.get_player_rating(int(player)))
            team_rating += player_rating
        team_id = int(team.split()[0])
        return team_rating, team_id


project_dir = os.listdir()
for folder in project_dir:
    is_test_dir = re.match('test_([A-Z])', folder)
    if is_test_dir:
        matchmaking = Matchmaker(folder)
        matchmaking.populate_teams()
        matchmaking.sort_list()
        matchmaking.rivals()
