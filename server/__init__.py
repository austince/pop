__author__ = 'austin'

from flask import Flask
from pop.corn import Maker, Robot

app = Flask(__name__)

app.debug = True

maker = Maker()

robot = Robot()

from server import endpoints
