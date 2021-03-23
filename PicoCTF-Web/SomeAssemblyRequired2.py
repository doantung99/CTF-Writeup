flag = ''
data = '''xakgK\\Ns><m:i1>1991:nkjl<ii1j0n=mm09;<i:u'''

for i in range(len(data)):
	flag += chr(ord(data[i])^8)

print(flag)
