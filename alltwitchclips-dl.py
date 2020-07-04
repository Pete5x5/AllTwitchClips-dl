import requests                 # Enable API request functionality
import subprocess               # Enable calling another process
import datetime                 # Enable date and time functionality
import os                       # Enable filesystem functionality
from pathlib import Path        # Enable filesystem path joining
import logging                  # Enable logging

creds = [line.strip() for line in open('creds.txt')]  # pull Twitch API credentials from creds.txt
cID = creds[0]  # Client ID from creds.txt
authCode = creds[1]  # Auth Code from creds.txt
redUri = creds[2]  # redirect uri from creds.txt

mainPath = Path(r"K:\media\Twitch\GordyKegs\Clips")  # path to the clips folder
logPath = mainPath/'logs'  # path to the logs folder

os.chdir(mainPath)  # change working directory to the clips folder

# LOGGING------
# gendate = (datetime.datetime.now()).strftime('%Y%m%d-%H%M%S')  # set the date and time to be added to log file
# logging.basicConfig(filename=str(logPath) + '/cliplog' + gendate + '.txt', level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')
# LOGGING------

baseurl = 'https://api.twitch.tv/helix/clips'  # URL for Twitch API (version helix)
numclips = 2  # number of clips per page, max 100
pagval = ''  # set pagination value to nothing by default
toPag = 0  # whether or not you want to paginate (default 1 = yes)
headers = {'redirect_uri': redUri, 'Client-ID': cID, 'Authorization': 'Bearer ' + authCode}  # headers for API request
urls = []  # make urls variable a list

while True:
    payload = {'broadcaster_id': '84842346', 'first': numclips, 'after': pagval}  # payload for API request
    r = requests.get(baseurl, headers=headers, params=payload)  # sends request to Twitch API using the base URL, headers, and payload
    resp = dict(r.json())  # get response in JSON format
    resppag = resp.get('pagination')  # get pagination info
    respdata = resp.get('data')  # get all clip data

    for x in range(len(respdata)):  # for each clip...
        datadict = dict(respdata[x])  # gets the first clip entry in dictionary format
        urls += [datadict['url']]  # find the URL for the clip
    if 'cursor' in resppag.keys() and toPag == 1:  # if there is a pagination value and pagination is enabled...
        pagval = resppag['cursor']  # set the pagination value and run again
    else:
        break

for x2 in range(len(urls)):  # for each URL...
    print(urls[x2])  # print the URL of the clip to be downloaded
    ytDL = subprocess.Popen(['python', '-m', 'youtube_dl', urls[x2], '-c', '-i', '--restrict-filenames', '--download-archive', 'gordy-vids', "-o'%(id)s_[]_%(title)s.%(ext)s'"])  # subprocess to run youtube-dl with the clip URL
    ytDL.wait()  # launch the subprocess, wait for it to finish before continuing