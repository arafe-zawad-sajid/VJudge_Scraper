from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import re
import datetime as dt

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

link = input('Enter vjudge contest link: ')
pieces = link.split('#')
url = pieces[0]+'#overview'

uhand = urlopen(url, context=ctx)
doc = uhand.read().decode()

timestamps = re.findall('<span class="timestamp">(.*)</span>', doc)
begin = dt.datetime.fromtimestamp(int(timestamps[0])/1e3)
end = dt.datetime.fromtimestamp(int(timestamps[1])/1e3)

title = re.findall('<title>(.*) - Virtual Judge</title>', doc)
title = title[0]

fpath = input('Enter file name: ')
if len(fpath)==0:
    fpath = title.lower()
    fpath = fpath.replace('bracu', '').replace('acm', '')
    fpath = re.sub('batch-\d*', '', fpath)
    fpath = re.sub('\d*/\d*/\d*', '', fpath)
    fpath = fpath.strip()

fpath = str(begin.date())+' '+fpath+'.txt'
fhand = open(fpath, 'w')
print('writing to', fpath)

fhand.write('Title: '+title+'\nLink: '+url+'\nfrom '+str(begin)+' to '+str(end)+'\n\nProblems:\n')

soup = BeautifulSoup(doc, 'html.parser')
tags = soup('td')
for tag in tags:
    if len(tag['class'])==2 and 'prob-num' in tag['class']:
        fhand.write(tag.get_text().strip()+'\t')
    if len(tag['class'])==2 and 'prob-origin' in tag['class']:
        fhand.write(tag.get_text().strip()+'\n')
print('done')
fhand.close()
