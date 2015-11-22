__author__ = 'austin'

from server import app, maker, robot
from flask import make_response, jsonify, request


@app.route('/time')
def time():
    return make_response(jsonify(time_remaining=maker.time_until_done()), 200)


@app.route('/make', methods=['GET', 'POST'])
def make():
    """
        Baddies:
            Maker is already running
            Robot is not back at the station

        Options:
            in request args
                pop_time
                sentiment
    :return:
    """

    pop_time = request.args.get('pop_time', None)
    sentiment = str(request.args.get('sentiment', 'neutral'))

    if maker.is_making():
        return make_response(jsonify(status="Failure",
                                     error="Maker is busy dog",
                                     time_left=maker.time_until_done()), 400)

    if pop_time is None:
        pop_time = maker.current_pop_time
    else:
        pop_time = float(pop_time)

    # Send the robot on finish
    maker.make_popcorn(pop_time, on_finish_function=robot.deliver)

    return make_response(jsonify(status="Great Success",
                                 pop_time=pop_time), 200)


@app.route('/command')
def command():
    pass
