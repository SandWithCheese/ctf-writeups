import SocketServer, threading, random, time

class ThreadedLotteryServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class LotteryHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        secret = random.Random()
        secret.seed(int(time.time())) 
        winning_choice = str(secret.random())
        self.request.sendall("Can you guess the number to win the flag lottery?\n")
        your_choice = self.request.recv(1024).strip()
        if winning_choice == your_choice:
            self.request.sendall("Congratulations you won the lottery! Have a flag!\n")
            self.request.sendall("%s\n" % open('flag.txt').readline().rstrip())
        else:
            self.request.sendall("Nope! The winning number was %s, better luck next time!\n" % winning_choice)
        return

if __name__ == '__main__':
    SocketServer.TCPServer.allow_reuse_address = True
    server = ThreadedLotteryServer(("0.0.0.0", 5000), LotteryHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server.serve_forever()
