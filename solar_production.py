#!/usr/bin/env python

#
# Monitors solar panel production and stores the 
# results in a database. The results can be viewed
# through a web page to display aggregate data,
# trends, etc.
#

import db
import monitor.vivint
import ui
import time

if __name__=="__main__":
    print "Main start"


    my_db = db.solar_db()
    mon = monitor.vivint.Monitor(my_db, period=5.0)

    mon.run()

    try:
        time.sleep(240)
        print "stopping..."
        mon.stop()
        print "waiting..."
        mon.join()
        
        print "Main exit"
    except KeyboardInterrupt:
        mon.stop()
        mon.join()
