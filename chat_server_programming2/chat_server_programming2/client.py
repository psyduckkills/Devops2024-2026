import socket
from threading import Thread
import os # kunna exit individuellt / varje klient individuellt 

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket() # Detta skapar en ny socket per klient
        self.running = True
        try:
            self.socket.connect((HOST, PORT)) # Ansluter till värd och port 
            print(f"Connected to server at {HOST}:{PORT}") 
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?") # Ifall man kör client filen först
            os._exit(1)

        self.name = input("Enter your name: ") # Skapar en tillfällig user 
        self.talk_to_server()

    def talk_to_server(self):
        try:
            self.socket.send(self.name.encode())
            receive_thread = Thread(target=self.receive_message) # Skapar en tråd
            receive_thread.start()
            self.send_message()
            receive_thread.join()  # Väntar på att tagna tråden avslutas
        except Exception as e: 
            print(f"Error while starting communication: {e}")
        finally:
            self.cleanup()

    def send_message(self):
        while self.running:
            try:
                client_input = input("")
                if not client_input.strip():
                    print("Message cannot be empty. Please type anything.")
                    continue

                client_message = f"{self.name}: {client_input}"
                self.socket.send(client_message.encode())
                if client_input.strip().lower() == "bye":
                    print("Exiting chat. Goodbye!")
                    self.running = False
                    break # Går ut från servern för att tillåta funktionen cleanup
            except (KeyboardInterrupt, BrokenPipeError):
                print("\nExiting chat. Goodbye!") # Felhantering 
                self.running = False
                break  

    def receive_message(self):
        while self.running:
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message.strip():
                    print("Server has closed the connection.")
                    self.running = False # self.running = True => programmet körs
                    break  # self.running = False => programmet avslutas
                else:
                    print("\033[1;32;40m" + server_message + "\033[0m") # Ger färg till chatten 
            except Exception as e:
                print(f"Error receiving message: {e}") # felhantering 
                self.running = False
                break  

    def cleanup(self):
        self.running = False
        try:
            self.socket.close()
        finally:
            os._exit(0)


if __name__ == '__main__':
    try:
        Client('127.0.0.1', 443)
    except KeyboardInterrupt:
        print("\nExiting client program. Goodbye!")







        


