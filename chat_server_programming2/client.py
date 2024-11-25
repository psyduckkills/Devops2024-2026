import socket
from threading import Thread
import os # kunna exit individuellt / varje klient individuellt 

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()# Detta skapar en ny socket per klient
        try:
            self.socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?") # Ifall man kör client filen först 
            os._exit(1)

        self.name = input("Enter your name: ")
        self.talk_to_server()

    def talk_to_server(self):
        try:
            # Skickar klientens username till servern 
            self.socket.send(self.name.encode())
            # Skapar en tråd för att få meddelanden 
            Thread(target=self.receive_message).start()
            # Start sending messages # Börjar skicka meddelanden 
            self.send_message()
        except Exception as e:
            print(f"Error while starting communication: {e}")
            os._exit(1)

    def send_message(self):
        while True:
            try:
                client_input = input("")
            except KeyboardInterrupt:
                print("\nClient exiting, Goodbye!")
                self.socket.close()
                os._exit(0)
            if not client_input.strip():
                print("Message cannot be empty. Please type anything.")
                continue

            client_message = self.name + ": " + client_input
            try:
                self.socket.send(client_message.encode())
                if client_input.strip().lower() == "bye":
                    print("Exiting chat. Goodbye!")
                    self.socket.close()
                    os._exit(0)
            except BrokenPipeError:
                print("Connection to the server lost. Exiting.")
                os._exit(1)

    def receive_message(self):
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message.strip():
                    print("Server has closed the connection.")
                    os._exit(0)
                print("\033[1;32;40m" + server_message + "\033[0m")
            except ConnectionResetError:
                print("Lost connection to the server.")
                os._exit(1)
            except Exception as e:
                print(f"Error receiving message: {e}")
                os._exit(1)

if __name__ == '__main__':
    try:
        Client('127.0.0.1', 443) 
    except KeyboardInterrupt:
        print("\nExiting client program. Goodbye!")
        os._exit(0)




        


