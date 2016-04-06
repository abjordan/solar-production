#!/usr/bin/env python

import bs4
import MySQLdb
import urllib2

import time
import datetime
import logging
import json
import threading

units = {
    "W": 1,
    "kW": 1000,
    "MW": 1000000,
    "Wh": 1,
    "kWh": 1000,
    "MWh": 1000000
}

def str_to_watts(s):
    tok = s.strip().split(" ")
    number = float(tok[0])
    unit = tok[1]
    watts = number * units[unit]
    return watts


class Monitor(object):

    def __init__(self, database, period=60.0):
        self.looper_thread = None
        self.keep_running = True
        self.period = float(period)
        self.event = threading.Event()
        self.db = database

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

        logging.warn("monitor loop starting")
        while self.keep_running:
            self.fetch_reading()
            sleep_time = self.period - (time.time() - start)
            if self.event.wait(sleep_time):
                break
            start = time.time()
        logging.warn("monitor loop exiting")

    def run(self):
        print "Starting up..."

        self.looper_thread = threading.Thread(target=self.read_loop)
        self.looper_thread.daemon = True
        self.looper_thread.start()


    def fetch_reading(self):
        response = urllib2.urlopen("http://192.168.1.3/production?locale=en")
        page = response.read()

        soup = bs4.BeautifulSoup(page, "html.parser", from_encoding='utf-8')

        current = soup.find('td', text="Currently").find_next('td').string
        today = soup.find('td', text="Today").find_next('td').string
        week = soup.find('td', text="Past Week").find_next('td').string
        install = soup.find('td', text="Since Installation").find_next('td').string

        data_point = { "current": str_to_watts(current),
                       "today": str_to_watts(today),
                       "week": str_to_watts(week),
                       "install": str_to_watts(install) }

        self.db.record_production(time.time(), data_point)
        
