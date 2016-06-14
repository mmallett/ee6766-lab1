#!/usr/bin/env python
import mraa
 
try:
    tempSensor = mraa.Aio(1)
    print (tempSensor.read()), "is the current temperature"
except KeyboardInterrupt:
    exit
 