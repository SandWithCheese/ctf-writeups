import socket, threading
from Crypto.Util.number import *
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time
import os
import random
from client_messages import client_messages

SERVER_SOCK = "/tmp/server"
ATTACKER_SOCK = "/tmp/attacker"

class Client:
	def __init__(self):
		self.client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client_socket.connect(ATTACKER_SOCK)

	def generateKey(self):
		self.parameters = dh.generate_parameters(generator=2, key_size=512)
		self.private_key = self.parameters.generate_private_key()
		self.public_key = self.private_key.public_key()
		self.sendparam()

	def deriveKey(self):
		self.derived_key = HKDF(
			algorithm=hashes.SHA256(),
			length=32,
			salt=None,
			info=b'handshake data',
		).derive(self.shared_key)

	def sendparam(self):
		self.serialized_parameters = self.parameters.parameter_bytes(serialization.Encoding.PEM, serialization.ParameterFormat.PKCS3)
		self.send(b"PARM||" + self.serialized_parameters.hex().encode())
		responseData = self.receive()
		if b"PARM_ACC" not in responseData:
			self.client_socket.close()
			exit()

	def loadparam(self):
		responseData = self.client_socket.recv(1024)
		if b"PARM||" in responseData[:6]:
			self.parameters = serialization.load_pem_parameters(bytes.fromhex(responseData[6:].decode()))
			self.send(b"PARM_ACC")
		else:
			self.client_socket.close()
			exit()

	def keyExchange(self):
		self.sendpubkey()
		self.recvpubkey()
		self.deriveKey()

	def sendpubkey(self):
		self.serialized_public_key = self.public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
		self.send(b"PUBK||" + self.serialized_public_key.hex().encode())
		responseData = self.receive()
		if b"PUBK_ACC" not in responseData:
			self.client_socket.close()
			exit()

	def recvpubkey(self):
		responseData = self.receive()
		if b"PUBK||" in responseData[:6]:
			self.holder_public_key = serialization.load_pem_public_key(
				bytes.fromhex(responseData[6:].decode()),
				backend=default_backend(),
			)
			self.shared_key = self.private_key.exchange(self.holder_public_key)
			self.send(b"PUBK_ACC")
		else:
			self.client_socket.close()
			exit()

	def initialization(self):
		self.hello()
		self.generateKey()
		self.keyExchange()

	def hello(self):
		self.send(b'hello!')
		response = self.receive()
		if response == b'hello!':
			return
		else:
			self.client_socket.close()
			exit()

	def main(self):
		self.initialization()		
		while True:
			self.sendmessage()
			self.recvmessage()

		self.client_socket.close()
		exit()

	def encrypt(self, message):
		iv = os.urandom(16)
		cipher = Cipher(algorithms.AES(self.derived_key), modes.CBC(iv), backend=default_backend())
		encryptor = cipher.encryptor()

		padder = padding.PKCS7(algorithms.AES.block_size).padder()
		padded_message = padder.update(message.encode()) + padder.finalize()

		ciphertext = iv + encryptor.update(padded_message) + encryptor.finalize()
		return base64.b64encode(ciphertext)

	def decrypt(self, message):
		message = base64.b64decode(message)
		iv = message[:16]
		message = message[16:]
		cipher = Cipher(algorithms.AES(self.derived_key), modes.CBC(iv), backend=default_backend())
		decryptor = cipher.decryptor()
		plaintext = decryptor.update(message) + decryptor.finalize()

		unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

		unpadded_message = unpadder.update(plaintext) + unpadder.finalize()

		return unpadded_message

	def send(self, message):
		time.sleep(1)
		self.client_socket.sendall(message)

	def sendmessage(self):
		message = random.choice(client_messages)
		data = self.encrypt(message)
		self.send(data)

	def receive(self):
		response = self.client_socket.recv(4096)
		if not response:
			self.client_socket.close()
			exit()
		return response

	def recvmessage(self):
		try:
			response = self.receive()
			data = self.decrypt(response).decode()
		except:
			self.client_socket.close()
			exit()



if __name__ == '__main__':
	client = Client()
	client.main()
