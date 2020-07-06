import requests                 # Enable API request functionality
import subprocess               # Enable calling another process
import datetime                 # Enable date and time functionality
import os                       # Enable filesystem functionality
from pathlib import Path        # Enable filesystem path joining
import logging                  # Enable logging
# breakpoint()                  # Debugging mode

configDict = dict()
configList = [line.strip().split(' = ') for line in open('config.txt')]  # pull run parameters from config.txt
for c1 in range(len(configList)):  # for each line in config file
    try:
        configDict[configList[c1][0]] = configList[c1][1]  # try to add the config setting to the dictionary
    except (IndexError, ValueError):
        continue  # if no value then skip it
numClips = int(configDict.setdefault('number-of-clips', '64')) # number of clips per page, max 100, default 64
if numClips > 100:
    numClips = 100
toPag = int(configDict.setdefault('pagination', '1'))  # whether or not you want to paginate (default 1 = yes)
if toPag != 0 and toPag != 1:  # check to make sure the value is 0 or 1
    toPag = 1
bID = configDict.setdefault('broadcaster-id', '84842346')  # broadcaster ID to find clips for
errLog = int(configDict.setdefault('error-logging', '0'))  # enable error logging?  default = 0 (no logging)
if errLog != 0 and errLog != 1:  # check to make sure the value is 0 or 1
    errLog = 0
clipLog = int(configDict.setdefault('clip-logging', '1'))  # enable clip logging?  default = 1 (log videos, do not attempt to download anything from a URL already in the log)
if clipLog != 0 and clipLog != 1:  # check to make sure the value is 0 or 1
    clipLog = 1

creds = [line.strip() for line in open('creds.txt')]  # pull Twitch API credentials from creds.txt
cID = creds[0]  # Client ID from creds.txt
authCode = creds[1]  # Auth Code from creds.txt
redUri = creds[2]  # redirect uri from creds.txt

mainPath = Path(r"K:\media\Twitch\GordyKegs\Clips")  # path to the clips folder
errorLogPath = mainPath/'error-logs'  # path to the logs folder
os.chdir(mainPath)  # change working directory to the clips folder

if errLog == 1:
    gendate = (datetime.datetime.now()).strftime('%Y%m%d-%H%M%S')  # set the date and time to be added to log file
    logging.basicConfig(filename=str(errorLogPath) + '/clipErrorLog' + gendate + '.txt', level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')  # enable logging and save the log in the errorLogPath

baseURL = 'https://api.twitch.tv/helix/clips'  # URL for Twitch API (version helix)
pagVal = ''  # set pagination value to nothing by default

headers = {'redirect_uri': redUri, 'Client-ID': cID, 'Authorization': 'Bearer ' + authCode}  # headers for API request
urls = []  # make urls variable a list

while True:
    payload = {'broadcaster_id': bID, 'first': numClips, 'after': pagVal}  # payload for API request
    r = requests.get(baseURL, headers=headers, params=payload)  # sends request to Twitch API using the base URL, headers, and payload
    resp = dict(r.json())  # get response in JSON format
    respPag = resp.get('pagination')  # get pagination info
    respData = resp.get('data')  # get all clip data

    for x in range(len(respData)):  # for each clip...
        dataDict = dict(respData[x])  # gets the first clip entry in dictionary format
        urls += [dataDict['url']]  # find the URL for the clip
    if 'cursor' in respPag.keys() and toPag == 1:  # if there is a pagination value and pagination is enabled...
        pagVal = respPag['cursor']  # set the pagination value and run again
    else:
        break

if clipLog == 1:  # if clip logging enabled
    try:
        cLog = [line.strip() for line in open('clip-log.txt')]  # load each line of clip log file if it exists
        print('clip log found')  # for debugging
    except (IndexError, ValueError, FileNotFoundError):  # if file cannot be loaded or there's an error...
        clipLogFile = open('clip-log.txt', 'w')  # make clip log file
        cLog = []  # make cLog an empty list
        print('clip log NOT found')  # for debugging
    newList = [w for w in urls if w not in cLog]  # make a new list from urls NOT already in the log
    clipLogFile = open('clip-log.txt', 'a')  # set log file to append mode
    print('append mode set')  # for debugging
    getURL = newList  # set the new list and the urls to download
else:
    getURL = urls  # if clip logging is not anables just use all urls found

for x2 in range(len(getURL)):  # for each URL...
    print(getURL[x2])  # print the URL of the clip to be downloaded
    ytDL = subprocess.Popen(['python', '-m', 'youtube_dl', getURL[x2], '-c', '-i', '--restrict-filenames', '--download-archive', 'gordy-vids', "-o'%(id)s_[]_%(title)s.%(ext)s'"])  # subprocess to run youtube-dl with the clip URL
    ytDL.wait()  # launch the subprocess, wait for it to finish before continuing
    if clipLog == 1:  # if clip logging enabled
        clipLogFile.write(getURL[x2] + '\n')  # append the url to the clip log file
        print('wrote to file ' + getURL[x2])  # for debugging