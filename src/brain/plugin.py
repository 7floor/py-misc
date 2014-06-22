def subscribe(message_pattern):
    """
    decorate function that will be called on messages matching given pattern
    may be applied multiple times for different patterns
    @subscribe('some/topic/pattern/#')
    def foo(message):
        pass
    """
    def add_pattern(func):
        if not hasattr(func, 'message_patterns'):
            func.message_patterns = []
        func.message_patterns.append(message_pattern)
        return func
    return add_pattern


def execute(func):
    """
    decorate function to be spawned as a greenlet
    @execute
    def run():
        pass
    """
    func.executable = True
    return func


def publish(topic, payload, qos=0, retain=False):
    """ publish to MQTT """
    pass


import ConfigParser
config = ConfigParser.ConfigParser()

import logging
logger = logging.getLogger()
