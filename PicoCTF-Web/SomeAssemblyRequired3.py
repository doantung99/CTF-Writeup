from itertools import cycle

key = "\xed\x07\xf0\xa7\xf1"
data = "\x9dn\x93\xc8\xb2\xb9A\x8b\xc2\x97\xd4f\xc7\x93\xc4\xd4a\xc2\xc6\xc9\xddb\x94\x9e\xc2\x892\x91\x90\xc1\xdd3\x91\x91\x97\x8bd\xc1\x92\xc4\x90"
flag = ''

decrypted = [chr(ord(a) ^ ord(b)) for (a,b) in zip(data, cycle(key))]
for i in decrypted:
	flag+=i

print(flag)