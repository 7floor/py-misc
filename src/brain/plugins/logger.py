from plugin import *


@subscribe('#')
def log(message):
    logger.debug("%s = %s", message.topic, message.payload)
