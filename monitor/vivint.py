#!/usr/bin/env python

import bs4
import urllib2

import time
import datetime
import logging
import json
import schedule
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

    def __init__(self, config, database, period=60.0):
        self.looper_thread = None
        self.keep_running = True
        self.config = config
        self.period = float(period)
        self.event = threading.Event()
        self.db = database
        self.scheduler = schedule.Scheduler()

    def join(self):
        if self.looper_thread:
            if self.looper_thread.is_alive():
                self.looper_thread.join()

    def stop(self):
        logging.info("VivintMonitor got stop signal")
        self.keep_running = False
        self.event.set()

    def read_loop(self):
        start = time.time()

        self.scheduler.every().day.at("23:00").do(self.fetch_eod_reading)
        self.scheduler.every(15).seconds.do(self.fetch_reading)

        logging.info("Monitor loop starting")
        while self.keep_running:
            self.scheduler.run_pending()
            time.sleep(1)
        logging.info("Monitor loop exiting")

    def run(self):
        logging.info("Starting Vivint monitoring module")

        self.looper_thread = threading.Thread(target=self.read_loop)
        self.looper_thread.daemon = True
        self.looper_thread.start()

    def pull_reading(self):
        response = urllib2.urlopen(self.config["monitor"]["address"])
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
        return data_point

    def fetch_eod_reading(self):
        '''Fetches the end of day reading'''
        try:
            data_point = self.pull_reading()
            self.db.record_eod(datetime.datetime.now(), data_point)        
        except Exception as e:
            logging.exception("EXCEPTION when getting end-of-day reading!")

    def fetch_reading(self):
        '''Fetches the intra-day reading'''
        try:
            data_point = self.pull_reading()
            self.db.record_production(datetime.datetime.now(), data_point)
        except Exception as e:
            logging.exception("EXCEPTION when getting regular reading!")
