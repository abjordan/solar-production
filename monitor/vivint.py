#!/usr/bin/env python

import bs4
import MySQLdb
import urllib2

import time
import datetime
import json
import threading

class Monitor(object):

    def __init__(self, period=60.0):
        self.keep_running = True
        self.period = float(period)

    def fetch_reading(self):
        print "Hello @ ", time.time()
        
    def stop(self):
        self.keep_running = False

    def read_loop(self):
        start = time.time()

        while self.keep_running:
            self.fetch_reading()
            sleep_time = self.period - (time.time() - start)
            time.sleep(sleep_time)
            start = time.time()

    def run(self):
        print "Starting up..."

        looper_thread = threading.Thread(target=self.read_loop)
        looper_thread.daemon = True
        looper_thread.start()

        try:
            while True and self.keep_running:
                time.sleep(5)
        except Exception, e:
            print "Interrupted: exiting"
            self.keep_running = False
            raise e
