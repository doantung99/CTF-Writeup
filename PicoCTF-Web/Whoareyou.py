#import library
import requests
import re

headers = {'User-Agent': 'PicoBrowser',
	       'Referer': 'http://mercury.picoctf.net:34588/',
	       'Date': '2018',
	       'DNT': '1',
	       'X-Forwarded-For': '2.16.66.0',
	       'Accept-Language': 'sv-SE'
	       }

r = requests.get('http://mercury.picoctf.net:34588/', headers=headers)
p = re.compile('picoCTF\{.*\}')
flag = p.findall(r.text)[0]
print(flag)