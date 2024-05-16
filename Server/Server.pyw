import socket
import threading as thread
import time

HOSTNAME = "127.0.0.1"
PORT = 9999
BUFFERDATI = 10240
TYPE = socket.SOCK_STREAM
FAMILY = socket.AF_INET

soc = socket.socket(FAMILY, TYPE)
soc.bind((HOSTNAME, PORT))
soc.listen()

print("Server in ascolto ...")

class Utente():
    def __init__(self, client: socket.socket):
        self.client = client
        self.closing = False
        self.reciveThread = thread.Thread(target=self.recive)
        self.reciveThread.start()

    def reply(self, message):
        reply(message)
    
    def recive(self):
        while(not self.closing):
            try:
                message = self.client.recv(BUFFERDATI)
                message = message.decode()
                if (message[0:1] == "/"):
                    match message:
                        case "/close": 
                            self.closing = True 
                            self.checkClose()
                else:
                    self.reply(message)
            except Exception as e:
                self.checkClose(e)
                time.sleep(10)

    def checkClose(self, e: Exception = ""):
        try:
            resolved = False
            if(self.closing):
                #self.reciveThread.
                close(self.client)
                resolved = True
            if not resolved:
                print(e)
        except Exception as ex:
            print(ex)
        

Client: dict[socket.socket] = dict()

def connection():
    while (running):
        (client_soc, indirizzo) = soc.accept()
        if not client_soc in Client:
            Client[client_soc] = Utente(client_soc) 

def reply(message: str):
    print(f"{message}")
    message = str(message)+"\n"
    for client in Client:
        client.sendall(message.encode())

def close(client: socket.socket):
    if client in Client.keys():
        client.close()
        Client[client] = "" 


def closeAll():
    running = False
    for client in Client:
        close(client)

def reload():
    closeAll()
    start()

def start():
    if not running:
        ConnectionThread.start()
        running = True

def consoleCommand():
    while(True):
        inputs = input("")
        data = "Console >>" + inputs.split(" ")
        match(data[0]):
            case "close": closeAll()
            case "reload": reload()
            case "start": start()
            case "say": reply(inputs[4:])  

try:
    running = True
    ConnectionThread = thread.Thread(target= connection)
    ConnectionThread.start()
    ConsoleCommand = thread.Thread(target=consoleCommand).start()

except Exception as e:
    print(e)

