#!/usr/bin/env python

#
# For storage of production data
# 

import logging

class solar_db(object):

    def __init__(self, config):
        self.config = config

    def record_eod(self, timestamp, reading):
        logging.info("Got EOD reading: '%s: %s'", timestamp, reading)
        pass

    def record_production(self, timestamp, reading):
        logging.info("Got reading: '%s: %s'", timestamp, reading)

        # Data is a dictionary with the keys:
        #   current
        #   today
        #   week
        #   install
        # Values are the production in watts

        pass
