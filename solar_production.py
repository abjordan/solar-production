#!/usr/bin/env python

#
# Monitors solar panel production and stores the 
# results in a database. The results can be viewed
# through a web page to display aggregate data,
# trends, etc.
#

import monitor.vivint
import ui
import time

if __name__=="__main__":
    print "Main start"

    mon = monitor.vivint.Monitor(period=10.0)

    mon.run()
    time.sleep(30)
    print "stopping..."
    mon.stop()
    print "waiting..."
    mon.join()

    print "Main exit"
    
