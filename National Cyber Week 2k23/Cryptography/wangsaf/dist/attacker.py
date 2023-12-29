import socket
import threading
import os

SERVER_SOCK = "/tmp/server"
ATTACKER_SOCK = "/tmp/attacker"

class Attacker:
	def handle_client(self):
		try:
			while True:
				client_data = self.client_socket.recv(4096)
				if not client_data:
					print('disconnected')
					exit()
				print('client:', client_data.decode())
				client_to_server = input("client (tamper): ").encode()
				if client_to_server == b"fw": #forward message
					client_to_server = client_data
				self.server_socket.sendall(client_to_server)
			self.attacker_socket.close()
		except:
			print("something's wrong")

	def handle_server(self):
		try:
			while True:
				server_data = self.server_socket.recv(4096)
				if not server_data:
					print('disconnected')
					exit()
				print('server:', server_data.decode())
				server_to_client = input("server (tamper): ").encode()
				if server_to_client == b"fw": #forward message
					server_to_client = server_data
				self.client_socket.sendall(server_to_client)
			self.attacker_socket.close()
		except:
			print("something's wrong")
	

	def handle_incoming(self):
		server_thread = threading.Thread(target=self.handle_server)
		server_thread.start()

		client_thread = threading.Thread(target=self.handle_client)
		client_thread.start()

	def main(self):
		try:
			os.remove(ATTACKER_SOCK)
		except OSError:
			pass
		try:
			attacker_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			attacker_socket.bind(ATTACKER_SOCK)
			attacker_socket.listen(1)
		
			self.client_socket, client_addr = attacker_socket.accept()
		
			self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self.server_socket.connect(SERVER_SOCK)
			
			self.handle_incoming()
		except:
			print("something's wrong")


if __name__ == '__main__':
	attacker = Attacker()
	attacker.main()
