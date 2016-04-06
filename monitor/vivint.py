#!/usr/bin/env python

import bs4
import MySQLdb
import urllib2

import time
import datetime
import logging
import json
import threading


class Monitor(object):

    def __init__(self, period=60.0):
        self.looper_thread = None
        self.keep_running = True
        self.period = float(period)
        self.event = threading.Event()

    def join(self):
        if self.looper_thread:
            if self.looper_thread.is_alive():
                self.looper_thread.join()

    def stop(self):
        logging.warn("GOT STOP")
        self.keep_running = False
        self.event.set()

    def read_loop(self):
        start = time.time()

        logging.warn("read loop starting")
        while self.keep_running:
            self.fetch_reading()
            sleep_time = self.period - (time.time() - start)
            if self.event.wait(sleep_time):
                logging.warn("Event is set")
                break
            start = time.time()
        logging.warn("read loop exiting")

    def run(self):
        print "Starting up..."

        self.looper_thread = threading.Thread(target=self.read_loop)
        self.looper_thread.daemon = True
        self.looper_thread.start()

    def fetch_reading(self):
        logging.warn("Hello @ %s", time.time())
        
