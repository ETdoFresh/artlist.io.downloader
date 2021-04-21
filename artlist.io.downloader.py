import os.path
import requests
import sys
import csv
from urllib.parse import urlparse

min_page = 1
max_page = 3
dest = '//ENAS/Media/Licensed/Artlist.io' # Directory to Save MP3s

# Log into artlist.io and get this data from the cookie request to an api... look /api/Song/List in network console
alArtist = 'sadfasdfasdfasdfasdfsa'
antiForgeryCookie = 'adsfadsfasfadsfaasfa'
xXsrfToken = 'asdfasdfadsfafasfasfdasfa'

headers = {
    'cookie': 'al-artlist=' + alArtist + '; AntiForgeryCookie=' + antiForgeryCookie,
    'x-xsrf-token': xXsrfToken,
    'Content-Type': 'application/json',
}

csvWriter = csv.writer(sys.stdout)

for i in range(min_page, max_page):
    # You can edit your search criteria here if you want... otherwise, I guess all?
    requestParams = """{"searchTerm":"",
 "categoryIDs":"",
 "excludedIDs":"",
 "songSortID":1,
 "page":""" + str(i) + """,
 "durationMin":0,
 "durationMax":0,
 "onlyVocal":null}"""
    resp = requests.post('https://artlist.io/api/Song/List', headers=headers, data=requestParams)
    json = resp.json()
    for song in json['songs']:
        url = urlparse(song['MP3FilePath'])
        filename = os.path.basename(url.path)
        csvWriter.writerow([song['artistName'], song['songName'], filename , song['MP3FilePath']])
        fullpath = os.path.join(dest, filename)
        if not os.path.exists(fullpath):
            download = requests.get(song['MP3FilePath'], allow_redirects=True)
            open(fullpath, 'wb').write(download.content)
