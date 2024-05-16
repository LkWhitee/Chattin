import socket
import threading
import datetime

HOSTNAME = "192.168.1.3"
PORT = 9999
BUFFERDATI = 10240
TYPE = socket.SOCK_STREAM
FAMILY = socket.AF_INET

# Create a socket object
soc = socket.socket(FAMILY, TYPE)
soc.bind((HOSTNAME, PORT))
soc.listen()

class Utente:
    def __init__(self, client: socket.socket):
        self.client = client
        self.closing = False
        self.reciveThread = threading.Thread(target=self.receive)
        self.Utente = ""
        self.reciveThread.start()

    def reply(self, message):
        reply(message)

    joinMessage = True

    def receive(self):
        while not self.closing:
            try:
                message = self.client.recv(BUFFERDATI)
                message = message.decode()
                if message[0:1] == "/":
                    if message == "/close":
                        self.closing = True
                        self.forceClose()
                else:
                    self.reply(message)

                if self.joinMessage:
                    self.joinMessage = False
                    message = message.split(" ")
                    self.Utente = message[0]
            except Exception as e:
                self.forceClose()
        
    def forceClose(self):
        reply(message=f"{self.Utente} left the chat", closed=self.client)
        close(self.client)

Client = {}
print("Server in ascolto ...")

def connection():
    while running:
        client_soc, indirizzo = soc.accept()
        if client_soc not in Client:
            Client[client_soc] = Utente(client_soc)

def reply(message: str, closed: socket.socket = None):
    with open("Log.log", "a+") as log:
        now = datetime.datetime.now()
        timestamp = now.strftime("%m-%d-%Y - %H:%M:%S")
        log.write(f"[{timestamp}] >> {message}\n")

    print(message)
    message = str(message) + "\n"
    if Client:
        for client in Client:
            if client != closed:
                try:
                    client.sendall(message.encode())
                except Exception as e:
                    print(f"Error sending message: {e}")

def close(client: socket.socket):
    if client in Client:
        del Client[client]
        client.close()

def closeAll():
    global running
    running = False
    for client in list(Client.keys()):
        close(client)

def reload():
    closeAll()
    start()

def start():
    global running
    if not running:
        running = True
        ConnectionThread = threading.Thread(target=connection)
        ConnectionThread.start()

def consoleCommand():
    while True:
        inputs = input("")
        data = inputs.split(" ")
        if data[0] == "close":
            closeAll()
        elif data[0] == "reload":
            reload()
        elif data[0] == "start":
            start()
        elif data[0] == "say":
            reply(" ".join(data[1:]))

try:
    running = True
    ConnectionThread = threading.Thread(target=connection)
    ConnectionThread.start()
    ConsoleCommand = threading.Thread(target=consoleCommand)
    ConsoleCommand.start()

except Exception as e:
    print(e)
