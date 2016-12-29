#!/usr/bin/env python

#
# For storage of production data
# 

import logging
import sqlite3

class solar_db(object):

    def __init__(self, config):
        self.config = config
        self.dbfile = self.config['database']['sqlite']['filename']
        self.create_tables()

    def get_conn(self):
        return sqlite3.connect(self.dbfile, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        
    def create_tables(self):
        with self.get_conn() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS currentProduction (ts timestamp, power INTEGER)''')
        
    def record_eod(self, timestamp, reading):
        '''Special call to indicate that this is the last data point you're going 
           to get today. Do any special end-of-day cleanup you need here.'''
        logging.info("Got EOD reading: '%s: %s'", timestamp, reading)
        pass

    def record_production(self, timestamp, reading):
        logging.info("Got reading: '%s: %s'", timestamp, reading)

        with self.get_conn() as conn:
            c = conn.cursor()
            c.execute("insert into currentProduction values (?, ?)",
                      (timestamp, reading['current']))
            c.close()

        # Data is a dictionary with the keys:
        #   current
        #   today
        #   week
        #   install
        # Values are the production in watts

        pass
