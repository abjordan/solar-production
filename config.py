#!/usr/bin/env python

import logging

config = {

    "logging": {
        "level": logging.DEBUG
    },
    
    "database": {
        "sqlite": {
            "filename": "solar.sqlite3"
        }
    },

    "monitor": {
        "address": "http://127.0.0.1:8000/sample.html"
    }
}
