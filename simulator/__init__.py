"""
-------------------------------------------------------
Simulator
a package that helps simulate a baseball game based on
previous batting history
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-11
-------------------------------------------------------
"""
import logging
from player import Player
from game import Game
from helpers import pstdev
import random
from copy import deepcopy
from pprint import PrettyPrinter
class Simulator():
    def __init__(self, file, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.import_players(file)
        self.pp = PrettyPrinter(indent=4)

    def import_players(self, file):
        # assuming csv
        self.girls = []
        self.boys = []
        with open(file) as f:
            for line in f:
                data = line.split(",")
                name = data[0]
                gender = data[1]
                hits = data[2:]
                if gender == "F":
                    self.girls.append(Player(name, hits, gender))
                else:
                    self.boys.append(Player(name, hits, gender))

    def run(self, lineups, games):
        stats = {}
        for options in  range(0, lineups):
            lineup = self.assemble_lineup()
            scores = []
            for game in range(0, games):
                scores.append(Game(lineup).run())
            stats[lineup] = (sum(scores)/games, pstdev(scores))
        self.pp.pprint(stats)

    def assemble_lineup(self):
        guy_count = 0
        girls = self.copy_list(self.girls)
        guys = self.copy_list(self.boys)
        lineup = []
        while len(girls) > 0 or len(guys) > 0:
            if len(girls) > 0  and len(guys) > 0 and guy_count < 4:
                coin = random.randint(0,1)
                if coin == 0:
                    lineup.append(girls.pop(random.randint(0, len(girls)-1)))
                else:
                    guy_count += 1
                    lineup.append(guys.pop(random.randint(0, len(guys) - 1)))
            elif len(girls) > 0:
                guy_count = 0
                lineup.append(girls.pop(random.randint(0, len(girls) - 1)))
            elif len(guys) > 0:
                lineup.append(guys.pop(random.randint(0, len(guys) - 1)))
        return lineup

    def copy_list(self, l):
        c = []
        for x in l:
            c.append(x)
        return c

import unittest
import os
class TestSimulator(unittest.TestCase):
    def setUp(self):
        directory = os.getcwd()
        while "simulator" in directory:
            directory = os.path.dirname(directory)
        directory = os.path.join(directory, "Tests")
        tests = ["test1.csv"]
        for test in tests:
            self.simulator = Simulator(os.path.join(directory,test))

    def tearDown(self):
        pass

    def testAssembleLineup(self):
        lineup = self.simulator.assemble_lineup()
        self.assertEqual(len(lineup), 3)

