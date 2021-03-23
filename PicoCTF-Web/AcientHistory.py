#import library
import requests
import re

flag = ''

#GET request
r = requests.get('http://mercury.picoctf.net:45211/')

#regex
p = re.compile('index\.html\?(.)\'\)')
for i in p.findall(r.text):
	flag += i

#Get flag from concatenation all character
print(flag)
