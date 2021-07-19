

#%%
import requests                 # Enable API request functionality
import subprocess               # Enable calling another process
import datetime                 # Enable date and time functionality
import os                       # Enable filesystem functionality
from pathlib import Path        # Enable filesystem path joining
import logging                  # Enable logging
# breakpoint()                  # Debugging mode

clipLog = clipDefault = 1  # enable clip logging?  default = 1 (log videos, do not attempt to download anything from a URL already in the log)

configDict = dict()
# configDict['clip-logging']='t'  # set clipLog to a letter in the above dict and see what happens (for testing)

#--------------#
# This whole thing should also go in the function
try:
    clipLog = int(configDict.setdefault('clip-logging', clipDefault))
except:
    clipLog = clipDefault
#-----------#

def valCheck(theVal, defVal):
    if theVal != 0 and theVal != 1:  # check to make sure the value is 0 or 1
        theVal = clipDefault  # if it's not, set it to the default value
    return theVal  # have the function return theVal when it exits
clipLog = valCheck(clipLog, clipDefault)  # set clipLog to the returned value
print(clipLog)

# ToDo
# use dict to associate var names with config parameters names (i.e. clipLog // 'clip-logging')
# use above dict value in setdefault
# add try and except with the import to the function
# call the function for each variable from the config file