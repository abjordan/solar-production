#!/usr/bin/env python

#import MySQLdb
import logging

class solar_db(object):

    def __init__(self):
        pass

    def record_production(self, timestamp, reading):
        logging.warn("Got reading: '%s: %s'", timestamp, reading)
