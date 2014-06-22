from plugin import *
import mysql.connector

@subscribe('#')
def log(message):
    logger.debug("%s = %s%s", message.topic, message.payload, (" (old)" if message.retain else ""))
    if not message.retain:
        con = mysql.connector.connect(autocommit=True, **params)
        cur = con.cursor()
        cur.callproc("log_mqtt_message", (message.topic, message.payload))
        con.close()


params = dict(config.items('MySQL'))