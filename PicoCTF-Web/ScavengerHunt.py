#import library
import requests
import re

#Get first part of the flag
r = requests.get('http://mercury.picoctf.net:55079')
p = re.compile('(of the flag|part \d): ([0-9a-zA-Z_{}]+)', flags=re.IGNORECASE)
part1 = p.findall(r.text)[0][1]

#Get second part of the flag
r = requests.get('http://mercury.picoctf.net:55079/mycss.css')
p = re.compile('part \d: ([0-9a-zA-Z_{}]+)', flags=re.IGNORECASE)
part2 = p.findall(r.text)[0]

#Get third part of the flag
r = requests.get('http://mercury.picoctf.net:55079/robots.txt')
p = re.compile('part \d: ([0-9a-zA-Z_{}]+)', flags=re.IGNORECASE)
part3 = p.findall(r.text)[0]

#Get fourth part of the flag
r = requests.get('http://mercury.picoctf.net:55079/.htaccess')
p = re.compile('part \d: ([0-9a-zA-Z_{}]+)', flags=re.IGNORECASE)
part4 = p.findall(r.text)[0]

#Get fifth part of the flag
r = requests.get('http://mercury.picoctf.net:55079/.DS_Store')
p = re.compile('part \d: ([0-9a-zA-Z_{}]+)', flags=re.IGNORECASE)
part5 = p.findall(r.text)[0]

#Get flag from concatenation all part
flag = part1 + part2 + part3 + part4 + part5
print(flag)