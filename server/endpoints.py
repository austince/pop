__author__ = 'austin'

from server import app, maker, robot, stopper
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
    stopper.shutoff()
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
    stopper.shutoff()
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
    stopper.start_listening()

    return make_response(jsonify(status="Great Success",
                                 maker_status=maker.get_status(),
                                 robot_status=robot.current_command(),
                                 pop_time=pop_time), 200)


@app.route('/shutStop')
def shutStop():
    """
        For emergency shutoff
    :return:
    """
    stopper.start_listening()
    stopper.shutoff()
    return make_response(jsonify(status="Great Success",
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
