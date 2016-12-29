#!/usr/bin/env python

#
# Monitors solar panel production and stores the 
# results in a database. The results can be viewed
# through a web page to display aggregate data,
# trends, etc.
#

import db
import logging
import monitor.vivint
import ui
import time

from config import config

if __name__=="__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=config['logging']['level'])
    logging.info("Main start")   

    my_db = db.solar_db(config)
    mon = monitor.vivint.Monitor(config, my_db, period=5.0)

    mon.run()

    try:
        time.sleep(24000)
        logging.info("stopping...")
        mon.stop()
        logging.info("waiting...")
        mon.join()
        logging.info("Main exit")
    except KeyboardInterrupt:
        mon.stop()
        mon.join()
