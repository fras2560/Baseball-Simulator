"""
-------------------------------------------------------
Game
a game object that is simulates on game
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-11
-------------------------------------------------------
"""
import logging
HITS = {"PF": -1, "GO": -1, "D": 2, "HR": 4, "S": 1, "K": -1}

class Game():
    def __init__(self, players, innings=5, logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.players = players
        self.innings = innings
        self.reset()
    
    def reset(self):
        self.inning = 1
        self.outs = 0
        self.bases = [0, 0, 0]
        self.score = 0
        self.atbat = 0

    def run(self):
        self.reset()
        while self.inning <= self.innings:
            hit = self.players[self.atbat].hit()
            if HITS[hit] > 0:
                self.advance_runners(HITS[hit])
            else:
                self.outs += 1
            # move through the order
            self.atbat = (self.atbat + 1) % len(self.players)
            # if three outs then inning is done
            if self.outs >= 3:
                self.logger.debug("-------------------------------")
                self.logger.debug("End of Inning %s" % self.inning)
                self.outs = 0
                self.clear_bases()
                self.inning += 1
        return self.score

    def run_p(self):
        self.reset()
        while self.inning <= self.innings:
            hit = self.players[self.atbat].hit_p()
            if HITS[hit] > 0:
                self.advance_runners(HITS[hit])
            else:
                self.outs += 1
            # move through the order
            self.atbat = (self.atbat + 1) % len(self.players)
            # if three outs then inning is done
            if self.outs >= 3:
                self.logger.info("-------------------------------")
                self.logger.info("End of Inning %s" % self.inning)
                self.outs = 0
                self.clear_bases()
                self.inning += 1
        self.logger.info("End score %s" % self.score)
        return self.score

    def advance_runners(self, advance):
        num = len(self.bases)
        # update runners
        for base in range(num - 1, -1, -1):
            if self.bases[base] != 0 and base + advance >= num:
                self.bases[base] = 0
                self.score += 1
            elif self.bases[base] != 0:
                self.bases[base] = 0
                self.bases[base + advance] = 1
        # add hitter onto bases
        if advance >= num:
            # homerun
            self.score += 1
        else:
            self.bases[advance-1] = 1
        return

    def clear_bases(self):
        self.bases = [0, 0, 0]
import unittest
from simulator.player import Player

class TestGame(unittest.TestCase):

    def setUp(self):
        self.players = [Player("X", ["HR"]),
                        Player("Y", ["D"]),
                        Player("Z", ["S"]),
                        Player("W", ["PF"])]
        self.game = Game(self.players, innings=1)

    def tearDown(self):
        pass

    def testAdvanceRunners(self):
        self.game.advance_runners(1)
        self.assertEqual(self.game.bases, [1, 0, 0], "Runner on first")
        self.game.advance_runners(2)
        self.assertEqual(self.game.bases, [0, 1, 1], "Runner should be 2&3")
        self.game.advance_runners(4)
        self.assertEqual(self.game.bases, [0, 0, 0], "Bases should be clear")

    def testRun(self):
        score = self.game.run()
        self.assertEqual(score, 7, "Score has to be 8")
        self.assertEqual(self.game.bases, [1, 0, 1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()