# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-4-20mA-Rx
#
#  You can find more information on our web site:
#   Yocto-4-20mA-Rx documentation:
#      https://www.yoctopuce.com/EN/products/yocto-4-20ma-rx/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yoctopuce.yocto_api import *
from yoctopuce.yocto_genericsensor import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any genericSensor sensor
    sensor = YGenericSensor.FirstGenericSensor()
    if sensor is None:
        die('No module connected')
else:
    sensor = YGenericSensor.FindGenericSensor(target + '.genericSensor1')

if not (sensor.isOnline()): die('device not connected')

# retreive module serial
serial = sensor.get_module().get_serialNumber()

# retreive both channels
channel1 = YGenericSensor.FindGenericSensor(serial + '.genericSensor1')
channel2 = YGenericSensor.FindGenericSensor(serial + '.genericSensor2')

while channel1.isOnline() and channel2.isOnline():
    print("channel 1:  %f %s" % (channel1.get_currentValue(), channel1.get_unit()))
    print("channel 2:  %f %s" % (channel2.get_currentValue(), channel2.get_unit()))
    print("  (Ctrl-C to stop)")
    YAPI.Sleep(1000)
YAPI.FreeAPI()
