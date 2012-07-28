"""
Extending on demo-03, implements an event callback we can use to process the
incoming data.

"""

import sys
import time

from ant.core import driver
from ant.core import node
from ant.core import event
from ant.core import message
from ant.core.constants import *

from config import *
from datetime import datetime, timedelta

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

from pymongo import Connection


# A run-the-mill event listener
class HRMListener(event.EventCallback):
    
    last_insertion_time = datetime.now()
    
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print 'Heart Rate:', ord(msg.payload[-1])
            if datetime.now() > self.last_insertion_time + timedelta(seconds = 10):
                print "Inserting"
                connection = Connection()
                db = connection.developerhealth
                doc = {'time': time.time(), 'value': ord(msg.payload[-1])}
                db.hrm.insert(doc)
                self.last_insertion_time = datetime.now()
            

# Initialize
stick = driver.USB2Driver(SERIAL)
antnode = node.Node(stick)
antnode.start()

# Setup channel
key = node.NetworkKey('N:ANT+', NETKEY)
antnode.setNetworkKey(0, key)
channel = antnode.getFreeChannel()
channel.name = 'C:HRM'
channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
channel.setID(120, 0, 0)
channel.setSearchTimeout(TIMEOUT_NEVER)
channel.setPeriod(8070)
channel.setFrequency(57)
channel.open()

# Setup callback
# Note: We could also register an event listener for non-channel events by
# calling registerEventListener() on antnode rather than channel.
channel.registerCallback(HRMListener())

# Wait
print "Listening for HR monitor events (120 seconds)..."
time.sleep(30)

# Shutdown
channel.close()
channel.unassign()
antnode.stop()
