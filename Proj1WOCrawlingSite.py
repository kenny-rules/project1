
# coding: utf-8

# In[3]:


import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import time
import re
import codecs

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

v = len(set(removeCapList))
print "Total count is : " + str(v)

