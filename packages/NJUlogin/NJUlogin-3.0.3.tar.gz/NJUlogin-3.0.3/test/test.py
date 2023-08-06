import execjs
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

pwdDefaultEncryptSalt = '4WdST1VUIDpZshmw'
passwd = '123456'
rds1 = 'nCbFFttJcPb5AJbjSYMYFBXmhskayfArmciiK4XFTC8A6P7dRRQnFBCX3nX4wRiM'
rds2 = 'PbssrJe2eJ4zJW72'
def encrypt(password, encrypt_salt):
	with open('encrypt.js', 'r') as f:
		script = ''.join(f.readlines())
	context = execjs.compile(script)
	return context.call('_gas', rds1+passwd, encrypt_salt, rds2)

print(encrypt(passwd, pwdDefaultEncryptSalt))

chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
def rds(length: int) -> str:
	return ''.join([random.choice(chars) for _ in range(length)])

def gas(data: str, key: str, iv: str) -> str:
	pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
	aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
	return base64.b64encode(aes.encrypt(pad_pkcs7)).decode('utf-8')

print(gas(rds1 + passwd, pwdDefaultEncryptSalt, rds2))