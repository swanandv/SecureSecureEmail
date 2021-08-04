from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES,PKCS1_OAEP

data = "This is an email".encode("utf-8")

print(data)

