
# coding: utf-8

# In[3]:


import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import time
import re
import codecs

def checkDate(partyDate,datecheck):
    nycDate = partyDate.find('span',attrs={'class': 'views-field views-field-created'}).text.strip()
    return datetime.strptime(nycDate,'%A, %B %d, %Y') < datecheck

def partyList(urlroot,pageNum):
    partylinklist = [] 
    url = urlroot+'/party-pictures?page='+str(pageNum)
    print 'Parsing '+url
    try:
        partyPage = urllib2.urlopen(url).read()
    except urllib2.HTTPError as e:
        print e.code
        time.sleep(30)
        partyPage = urllib2.urlopen(url).read()
    soup = BeautifulSoup(partyPage)
    partylist = soup.find('div',attrs={'class': 'view-content'})
    parties = partylist.find_all('div',attrs={'class': 'views-row'})
    for p in parties:
        if checkDate(p,datetime(2014, 12, 1, 0,0)):
          partyLink = urlroot+p.find('a').attrs['href']
          if partyLink != 'http://www.newyorksocialdiary.com/nysd/partypictures':
              partylinklist.append(partyLink)
    return partylinklist

for page in np.arange(1,26):
    parties = partyList("http://newyorksocialdiary.com",page)
    
def getCaptions(purl):
    caplist=[];
    try:
        page = urllib2.urlopen(purl).read()
    except urllib2.HTTPError as e:
        print e.code
        time.sleep(30)
        page = urllib2.urlopen(purl).read()
    findCaption = BeautifulSoup(page)
    findDivCaption = findCaption.find_all('div', attrs={'class': 'photocaption'})
    findIdCap = findCaption.find_all('div', attrs={'id': 'photocaption'})
    findClassCaptions = findCaption.find_all('td', attrs={'class': 'photocaption'})
    findByFont = findCaption.find_all('font', attrs={'face': 'Verdana, Arial, Helvetica, sans-serif','size': '1'})
    nycCaptions=findDivCaption+findIdCap+findClassCaptions+findByFont    
    for c in nycCaptions:
        caplist.append(re.sub(r"(\s\s)+",' ',c.text).strip())
    return list(set(caplist))
        
def scapeNyds():
    urlroot = "http://www.newyorksocialdiary.com"
    for page in np.arange(1,26):
        captions = []
        parties = partyList(urlroot,page)
        for p in parties:
            captions = captions+getCaptions(p)
        fileName = 'partypage%02i' % page
        f = codecs.open(fileName,mode='wb',encoding='utf-8')
        for c in captions:
             f.write(c+'\n')
        f.close()     

scapeNyds()  

def loadPages():
    newcaps = []
    for page in np.arange(1,26):
        f = codecs.open('partypage%02i'%page, encoding='utf-8')
        for line in f:
            newcaps.append(re.sub(r'\n','',line))
        f.close()
    return newcaps

def removeExcessCaptions(caps):
    for c in caps:
        if len(c) > 250:
            caps.remove(c)
        elif re.match('Photo',c):
            caps.remove(c)
        elif re.match('Click',c):
            caps.remove(c)
        elif c =='':
            caps.remove(c)

def cleanCaptions(c):
    c = re.sub('\s+', ' ', c)
    c = re.sub('\(.+\)','',c)
    c = re.sub('\[.+\]','',c)
    c = re.sub('\.','',c)
    c = re.sub(r"(Philanthro\w+ |Trustees |Sundance |Host |Co-Chairm[ea]n |Board |Mr |Mrs |Founder |founder |Smithsonian |Secretary |Chairs |Gala |Baroness |Baron |Mayor |Co-chairs |Honorable |Vice |Diretor |director |Principal |Museum |Magician |Senior |Lady |Sir |Event |Exec |exec |Prince* |King |Chairman |Chairmen |honoree |Honoree |Governor |Commissioner |Trustee | trustee |President |Speaker |Dr |Doctor |Ambassador |Senator |Excellency |Executive |executive |Committee |committee |Chair |chair |Associate |[Mm]ember[s]* |[A-H|J-Z]{2,})",'',c)
    c = re.sub('\s+with\s+([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)$',r',\1 \3,\2 \3',c)  
    c = re.sub('\s+and\s+([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)$',r',\1 \3,\2 \3',c)
    c = re.sub('^([A-Z][a-z]+),\s+([A-Z][a-z]+),\s+([A-Z][a-z]+),\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r'\1 \5,\2 \5,\3 \5,\4 \5',c)
    c = re.sub('^([A-Z][a-z]+),\s+([A-Z][a-z]+),\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r'\1 \4,\2 \4,\3 \4',c)
    c = re.sub('^([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r'\1 \3,\2 \3',c)
    c = re.sub('[,:;.]\s+([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r',\1 \3,\2 \3,',c)
    c = re.sub('^([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+with\s+([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r'\1 \2,\3 \5,\4 \5',c)    
    c = re.sub('[,:;.]\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+with\s+([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)',r'\1 \2,\3 \5,\4 \5',c)     
    c = re.sub('^([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+with\s+([A-Z][a-z]+)',r'\1 \2,\3 \2',c)
    c = re.sub('[,:;.]\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+with\s+([A-Z][a-z]+)',r'\1 \2,\3 \2',c)   
    c = re.sub('\s+and\s+',',',c)
    c = re.sub('\s+with\s+',',',c)
    c = re.sub('\s*,\s+',',',c)
    c = re.sub(',,',',',c)
    c = re.sub('^[\s+|,]','',c)
    c = re.sub(',and\s+',',',c)
    c = re.sub('([\s,][Hh]is |[\s,][Hh]er |[\s,][Tt]heir |[\s,][Tt]he )',' ',c)
    return c
            
capList = loadPages()
removeExcessCaptions(capList)
removeCapList = [cleanCaptions(x) for x in capList]
len(set(removeCapList))


# In[26]:


len(set(namesOf))

