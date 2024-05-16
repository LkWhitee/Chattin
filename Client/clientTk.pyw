import threading as thread
import socket as soc
import tkinter as tk
from tkinter import messagebox
import time
import public_ip

class EntryWithPlaceHolder:
    def __init__(self, master, placeholder, row=0, column=0, padx=0, pady=0, columnspan=1, width=20):
        self.placeholder = placeholder
        self.Entry = tk.Entry(master, width=width)
        self.Entry.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
        self.add()
        self.Entry.bind('<FocusIn>', self.erase)
        self.Entry.bind('<FocusOut>', self.add)

    def erase(self, event=None):
        if self.Entry.get() == self.placeholder:
            self.Entry.delete(0, 'end')
            self.Entry.configure(fg="#000000")

    def add(self, event=None):
        if self.Entry.get() == '':
            self.Entry.insert(0, self.placeholder)
            self.Entry.configure(fg="#c2c2c2")

    def getVar(self):
        return self.Entry.get()

    def getEntry(self):
        return self.Entry

    def setFocus(self, event=None, args=None):
        self.Entry.focus_set()

    def clear(self):
        self.Entry.delete(0, 'end')


BUFFERDATI = 10240

connected = False
firstTime = True
flagIp = False
flag = True
threadrunning = True

def connect(event=None):
    global ip, socketClient, connected, firstTime, flag, flagIp, threadrunning

    if firstTime:
        firstTime = False
        while flag:
            try:
                ip = public_ip.get()
                flagIp = True
                flag = False
                print(ip)
            except Exception as e:
                flag = messagebox.askyesno(
                    "Ip Error",
                    f"{e}; \nIn caso di errore persistente contattare email: tommasopillonn@gmail.com \nVuoi riprovare?"
                )

    if flagIp:
        try:
            hostname = entryHostArea.getEntry().get()
            port = int(entryPortArea.getEntry().get())
            socketClient = soc.socket()
            socketClient.connect((hostname, port))
            connected = True
            
            s = thread.Thread(target=recivingMessage, daemon=True).start()
           
            print("Connected")
            checkStatus()
            sendMessage(message=f"{ip} joined the chat")
        except Exception as e:
            messagebox.showwarning(
                "Connection Error",
                f"{e} \n in caso di errore persistente contattare email:tommasopillonn@gmail.com"
            )

def disconnect():
    global connected

    if connected:
        sendMessage(message="/close")
        time.sleep(1)
        connected = False
        socketClient.close()
        writeMessage(f"{ip} left the chat\n")
    checkStatus()

def sendMessage(event=None, message=" "):
    global connected
    if connected:
        if message == " ":
            message = str(f"{ip} >> " + entryMessage.getEntry().get())
            entryMessage.clear()
        if message.strip():
            socketClient.sendall(message.encode())

def checkStatus():
    if connected:
        statusLabel.config(text="Status Online", fg="green")
    else:
        statusLabel.config(text="Status Offline", fg="red")

def recivingMessage():
    global connected
    while connected:
        try:
            dato = socketClient.recv(BUFFERDATI)
            if dato:
                dato = dato.decode()
                writeMessage(dato)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    disconnect()

def writeMessage(message: str):
    textArea.config(state='normal')
    textArea.insert("0.0", message)
    textArea.config(state='disabled')

def clear():
    textArea.delete("1.0", tk.END)

def on_closing():
    disconnect()
    if messagebox.askokcancel("Quit", "Vuoi uscire?"):
        root.destroy()
        time.sleep(1)

def startconnection(e=None):
    connectionThread = thread.Thread(target=connect, daemon=True)
    connectionThread.start()

root = tk.Tk()
root.resizable(False, False)
root.geometry("400x850")
root.title("Client")

entryHostArea = EntryWithPlaceHolder(root, placeholder="Hostname", row=0, column=0)
entryPortArea = EntryWithPlaceHolder(root, placeholder="Port", row=0, column=1)
entryHostArea.getEntry().bind("<Return>", entryPortArea.setFocus)
entryPortArea.getEntry().bind("<Return>", connect)
entryMessage = EntryWithPlaceHolder(root, placeholder="Message", row=1, column=0, columnspan=2, width=40)
entryMessage.getEntry().bind("<Return>", sendMessage)
statusLabel = tk.Label(root, text="Status Offline", fg="red")
statusLabel.grid(row=0, column=3)

textArea = tk.Text(root, width=50, height=50, state='disabled')
textArea.grid(row=2, columnspan=4)

buttonConnect = tk.Button(root, text="Connect", command=startconnection).grid(row=0, column=2)
buttonSend = tk.Button(root, text="Send", command=sendMessage).grid(row=1, column=2)
buttonDisconnect = tk.Button(root, text="Disconnect", command=disconnect).grid(row=1, column=3)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
