import threading as thread
import socket as soc
import tkinter as tk
from tkinter import messagebox
import time
import requests

class EntryWithPlaceHolder():
    placeholder = None
    master = None
    row = None
    column = 0
    Entry = None

    def erase(self, event=None):
        if self.Entry.get() == self.placeholder:
            self.Entry.delete(0,'end')
            self.Entry.configure(fg="#000000")

    def add(self, event=None):
        if self.Entry.get() == '':
            self.Entry.insert(0, self.placeholder)
            self.Entry.configure(fg="#c2c2c2")

    def __init__(self, master, placeholder, row = 0, column = 0, padx = 0, pady = 0, columnspan = 1):
        self.master = master
        self.placeholder = placeholder
        self.Entry = tk.Entry(master)
        self.Entry.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
        self.add()
        self.Entry.bind('<FocusIn>', self.erase)
        self.Entry.bind('<FocusOut>', self.add)
        

    def getVar(self):
        return self.Entry.get()
    
    def getEntry(self):
        return self.Entry
    
    def setFocus(self, event = None, args = None):
        self.Entry.focus_set()

    def clear(self):
        self.Entry.delete(0,'end')

BUFFERDATI = 10240

PortEx = " "
connected = False
firstTime = True
def connect(event = None):
    global ip, socketClient, connected, PortEx, firstTime
    if firstTime:
        firstTime = False
        ip = requests.get('http://ip.42.pl/raw').text
        print(ip)
        

    hostname = entryHostArea.getEntry().get()
    port = int(entryPortArea.getEntry().get())
    if (PortEx != port):
        PortEx = port
        socketClient = soc.socket()
        socketClient.connect((hostname, port))
        connected = True
        recivingMessageThread.start()
        print("Connected")
        checkStatus()
        sendMessage(message=f"{ip} joined the chat")

def disconnect():
    global connected
    if connected:
        sendMessage(message="/close")
        time.sleep(1)
        connected = False
        socketClient.close()
    checkStatus()

def sendMessage(event = None, message : str = " "):
    if connected:
        if message == " ":
            if message[0:6] == "/":
                disconnect()
            message = str(f"{ip} >> " + entryMessage.getEntry().get())
        socketClient.sendall(message.encode())
    

def checkStatus():
    if connected:
        statusLabel.config(text="Status Online", fg="green")
    else:
        statusLabel.config(text="Status Offline", fg="red")

def recivingMessage():
    global connected
    while(connected):
        
        dato = socketClient.recv(BUFFERDATI)
        dato = dato.decode()
        writeMessage(dato)

def writeMessage(message: str):
    global textArea
    textArea.config(state='normal')
    textArea.insert("0.0", message)
    textArea.config(state='disabled')


def clear():
    global textArea
    textArea.delete("1.0", tk.END)


def on_closing():
    disconnect()
    if messagebox.askokcancel("Quit", "Vuoi uscire?"):
        root.destroy()
        time.sleep(3)

def startconnection(e = None):
    connectionThread = thread.Thread(target=connect)
    connectionThread.start()

root = tk.Tk()
root.geometry("500x500")
root.title("Client")

entryHostArea = EntryWithPlaceHolder(root, placeholder="Hostname", row=0, column=0)
entryPortArea = EntryWithPlaceHolder(root, placeholder="Port", row=0, column=1)
entryHostArea.getEntry().bind("<Return>", entryPortArea.setFocus)
entryPortArea.getEntry().bind("<Return>", connect)
entryMessage = EntryWithPlaceHolder(root, placeholder="Message", row=1, column=0, columnspan=2)
entryMessage.getEntry().bind("<Return>", sendMessage)
statusLabel = tk.Label(root, text="Status Offline", fg="red")
statusLabel.grid(row=1, column=3)


textArea = tk.Text(root, width=50, height=50, state='disabled')
textArea.grid(row=2, columnspan=4)

buttonConnect = tk.Button(root, text="Connect", command=startconnection).grid(row=0, column=2)
buttonSend = tk.Button(root, text="Send", command=sendMessage).grid(row=1, column=1)
buttonClear = tk.Button(root, text="Clear", command=clear).grid(row=1, column=2)

recivingMessageThread = thread.Thread(target = recivingMessage)
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()