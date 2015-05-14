"""
-------------------------------------------------------
Player
a player object holds all the information about a player
-------------------------------------------------------
Author:  Dallas Fraser
ID:      110242560
Email:   fras2560@mylaurier.ca
Version: 2014-09-11
-------------------------------------------------------
"""
HITS = ["S","D", "GO", "PF", "HR"]
import logging
from random import randint

class Player():
    def __init__(self, name, hits, gender="M", logger=None):
        if logger is None:
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.name = name
        self._process_hits(hits)
        self.gender = gender

    def _process_hits(self, hits):
        count = {}
        recognized = 0 
        for hit in HITS:
            count[hit] = 0
        for hit in hits:
            hit = hit.strip()
            if hit in count:
                count[hit] += 1
                recognized += 1
            else:
                self.logger.error("Did not-recognize hit %s by %s" % 
                                  (hit, self.name))
        self.lookup = []
        if recognized   >  0 :
            for hit, tally in count.items():
                for i in range(0, int(100 * tally/len(hit))):
                    self.lookup.append(hit)
            self.length = len(self.lookup)
            self.logger.debug("Lookup:"  + " ".join(self.lookup))
        else:
            self.logger.error("No hits were recongized")
            raise Exception("No hits")

    def __str__(self):
        return self.name

    def hit(self):
        hit = self.lookup[randint(0, self.length - 1)]
        self.logger.debug("%s with a %s" % (self.name, hit))
        return hit

    def is_girl(self):
        return self.gender == "F"
        
import unittest
class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.hits = ["S", "D", "HR", "GO", "PF"]

    def tearDown(self):
        pass

    def testConstructor(self):
        self.player = Player("Dallas Fraser", self.hits)
        try:
            self.player = Player("Dallas Fraser", ["XX"])
            self.assertEqual(True, False, "Exception should have been raised")
        except:
            pass

    def testHit(self):
        self.player = Player("Dallas Fraser", self.hits)
        hit = self.player.hit()
        self.assertEqual(hit in self.hits, True )
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()