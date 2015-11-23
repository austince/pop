__author__ = 'austin'

from flask import Flask
from pop.corn import Maker, Robot, Stopper
import json

app = Flask(__name__)

app.debug = True

maker = Maker()

robot = Robot()


def finish_pop():
    """
        Called if the arduino senses that all the popcorn has popped
        Should be called by Stopper
        Super Dirty
    :return:
    """
    if not maker.is_making():
        print "Is making pop!"

    time_left = maker.time_until_done()
    print "Stopping maker with " + str(time_left) + " seconds left"
    maker.stop()
    robot.deliver()
    print "Great Success"


stopper = Stopper(stop_function=finish_pop)

from server import endpoints
