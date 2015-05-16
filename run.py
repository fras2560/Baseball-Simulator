from simulator import Simulator
from pprint import PrettyPrinter
import os
import logging
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
directory = os.getcwd()
directory = os.path.join(directory, "Tests")
file = os.path.join(directory, "Team.csv")
s = Simulator(file, logger=logger)
s.run(100, 1000)