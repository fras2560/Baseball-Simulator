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
from simulator.player import Player
from simulator.game import Game
from simulator.helpers import pstdev
import random
from copy import deepcopy
from pprint import PrettyPrinter
import sys
from simulator.tqdm import tqdm

SEPERATOR = "----------------------------------------"
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
                if gender.strip().upper() == "F":
                    self.girls.append(Player(name,
                                             hits,
                                             gender,
                                             logger=self.logger))
                else:
                    self.boys.append(Player(name,
                                            hits,
                                            gender,
                                            logger=self.logger))

    def run(self, lineups, games):
        self.stats = []
        for options in  tqdm(range(0, lineups)):
            #self.update_progress(options, lineups)
            lineup = self.assemble_lineup()
            scores = []
            for game in range(0, games):
                score = Game(lineup, logger=self.logger).run()
                scores.append(score)
            self.stats.append((sum(scores)/games, pstdev(scores), lineup))
        self.display_results()

    def display_results(self):
        optimal = self.find_agressive()
        conservative = self.find_conservative()
        print("Conservative: {0:.2f} +- {1:.2f}".format(conservative[0], conservative[1]))
        print(SEPERATOR)
        for player in conservative[2]:
            print(player)
        print(SEPERATOR)
        print("Agressive: {0:.2f} +- {1:.2f}".format(optimal[0], optimal[1]))
        print(SEPERATOR)
        for player in optimal[2]:
            print(player)
        print(SEPERATOR)
        print("Simulation of Conservative")
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        Game(conservative[2], logger=self.logger).run_p()

    def update_progress(self, runs, total):
        progress = runs / total
        sys.stdout.write("\r{0:.2f}%".format(progress))
        sys.stdout.flush()

    def find_agressive(self):
        result = self.stats[0]
        for sim in self.stats:
            if sim[0] > result[0]:
                result = sim
        return result

    def find_conservative(self):
        result = self.stats[0]
        for sim in self.stats:
            if sim[0]- 3*sim[1] > result[0] - 3 * result[1]:
                result = sim
        return result
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

