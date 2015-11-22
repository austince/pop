from server import messages as m
from random import randint


def make_message(sentiment):
    """
        Just get a random message from the bank
    :param sentiment: str, either neg, pos, or neutral
    :return: a message
    """
    if sentiment == "pos":
        messages = m.pos
    elif sentiment == "neg":
        messages = m.neg
    elif sentiment == "neutral":
        messages = m.neutral
    else:
        raise ValueError(sentiment + " is no sentiment of mine!")

    return messages[randint(0, len(messages)-1)]
