__author__ = 'austin'

from flask import Flask
from pop.corn import Maker, Robot, Stopper

app = Flask(__name__)

app.debug = True

maker = Maker()

robot = Robot()

stopper = Stopper()

from server import endpoints
