import requests

creds = [line.strip() for line in open('creds.txt')]  # pull Twitch API credentials from creds.txt
cID = creds[0]  # Client ID from creds.txt
authCode = creds[1]  # Auth Code from creds.txt
redUri = creds[2]  # redirect uri from creds.txt

baseurl = 'https://api.twitch.tv/helix/clips'  # URL for Twitch API (version helix)
numclips = 2  # number of clips per page, max 100
pagval = ''  # set pagination value to nothing by default
toPag = 0  # whether or not you want to paginate (default 1 = yes)
headers = {'redirect_uri': redUri, 'Client-ID': cID, 'Authorization': 'Bearer ' + authCode}
urls = []

while True:
    payload = {'broadcaster_id': '84842346', 'first': numclips, 'after': pagval}
    r = requests.get(baseurl, headers=headers, params=payload)  # sends request to Twitch API using the base URL, headers, and payload
    resp = dict(r.json())  # get response in JSON format
    resppag = resp.get('pagination')  # get pagination info
    respdata = resp.get('data')  # get all clip data

    for x in range(len(respdata)):
        datadict = dict(respdata[x])  # gets the first clip entry in dictionary format
        urls += [datadict['url']]  # find the URL for the clip
    if 'cursor' in resppag.keys() and toPag == 1:  # if there is a pagination value and pagination is enabled...
        pagval = resppag['cursor']  # set the pagination value and run again
    else:
        break
print(urls)

# for x2 in range(len(urls)):