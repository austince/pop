__author__ = 'austin'

from server import app, maker, robot
from server.util import make_message
from flask import make_response, jsonify, request


@app.route('/time')
def time():
    return make_response(jsonify(time_remaining=maker.time_until_done(),
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command()), 200)


@app.route('/stop', methods=['GET', 'POST'])
def stop():
    """

    :return:
    """
    #  Todo: kill the thread as well
    maker.stop()
    return make_response(jsonify(status="Great Success",
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command()), 200)


@app.route('/comeback')
def reset():
    """
        Reset everything to off/stationary
    :return:
    """
    maker.stop()
    robot.stay()
    return make_response(jsonify(status="Great Success",
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command()), 200)


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
    print "sentiment " + sentiment
    if maker.is_making():
        return make_response(jsonify(status="Failure",
                                     maker_status=maker.get_status(),
                                     robot_status=robot.current_command(),
                                     error="Maker is busy dog",
                                     error_type="busy",
                                     time_left=maker.time_until_done()), 400)

    if pop_time is None:
        pop_time = maker.default_pop_time
    else:
        pop_time = float(pop_time)

    # Send the robot on finish
    robot.set_message(make_message(sentiment))
    maker.make_popcorn(pop_time, on_finish_function=robot.deliver)

    return make_response(jsonify(status="Great Success",
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command(),
                                 pop_time=pop_time), 200)


@app.route('/finishedPopping', methods=['POST'])
def finish_pop():
    """
        Called if the arduino senses that all the popcorn has popped
    :return:
    """
    if not maker.is_making():
        return make_response(jsonify(status="Failure",
                                     maker_status=maker.get_status(),
                                     robot_status=robot.current_command(),
                                     error="Maker isn't running dog",
                                     error_type="inactive"), 400)

    time_left = maker.time_until_done()
    print "Stopping maker with " + str(time_left) + " seconds left"
    maker.stop()
    robot.deliver()
    return make_response(jsonify(status="Great Success",
                                 time_left=time_left,
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command()), 200)


@app.route('/comeback')
def comeback():
    message = request.args.get('message', "I'm coming home. Tell the world.")

    robot.come_back(message=message)
    return make_response(jsonify(status="Great Success",
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command()), 200)


@app.route('/command')
def command():
    """
        Doing call / response for now, not messing around with push notifications
        though probably would in future

        @see pop.corn.Robot
    :return:
    """
    return make_response(jsonify(robot.current_command()), 200)
