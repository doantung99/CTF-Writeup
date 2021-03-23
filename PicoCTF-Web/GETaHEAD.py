#import library
import requests

#HEAD request
r = requests.head('http://mercury.picoctf.net:28916')

#Get flag in response header
print(r.headers['flag'])