import socket
from threading import Thread
import time

class Server:
    Clients = [] # skapar en tom lista för klienter 

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT)) # Binder socket till en specifik värd och port
        self.socket.listen() # Lyssnar på flera länkade klienter. Om man skrev listen(5) så kan man ansluta 5 klienter till servern 
        print(f"Server started on {HOST}:{PORT}. Awaiting connections...")
        self.threads = []
        self.running = True 

    def listen(self):
        try:
            while self.running:
                self.socket.settimeout(1)
                try:
                    client_socket, address = self.socket.accept()
                    print(f"Connected to user at {address}")
                    print(f"Currently connected clients: {len(Server.Clients)}")

                    client_name = client_socket.recv(1024).decode().strip()
                    client = {'client_name': client_name, 'client_socket': client_socket}
                     # Skriver att en ny client är med chat servern, eller en existerande 
                    self.broadcast_message(client_name, f"{client_name} has joined the chat!")
                    Server.Clients.append(client) # Detta ligger klienten i Class Server i Client listan 

                    thread = Thread(target=self.handle_new_client, args=(client,)) 
                    thread.start() # Skapar en tråd som skapar, enskilda stängingar av chattarna. 
                    self.threads.append(thread)
                except socket.timeout:
                    continue
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Shutting down server...")
            self.shutdown()

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            try:
                client_message = client_socket.recv(1024).decode().strip()  # .lower för att ta emot fler stiliseringar (Bye, bYe ect)
                self.broadcast_message(client_name, f"{client_name} has left the chat.")
                if not client_message or client_message.lower() == f"{client_name}: bye": # Om man skriver bye kan
                    self.broadcast_message(client_name, f"{client_name} has left the chat.") #man gå ur chatten
                    Server.Clients.remove(client) 
                    client_socket.close()
                    break
                else:
                    self.broadcast_message(client_name, client_message)
            except Exception as e:
                print(f"Error with {client_name}: {e}") # Ifall anslutiningen inte funkar så tar man bort klienten
                Server.Clients.remove(client)
                client_socket.close()
                break

    def broadcast_message(self, sender_name, message):
        disconnected_clients = [] 
        
        for client in Server.Clients:
            client_socket = client['client_socket']
            client_name = client['client_name']
            if client_name != sender_name:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error sending to {client_name}: {e}")
                    disconnected_clients.append(client)
        
        for client in disconnected_clients:
            Server.Clients.remove(client)

    def shutdown(self):
        # Informerar alla klienter av att servern stängs
        self.broadcast_message("SERVER", "Server is shutting down. Goodbye!")
        
        # Detta gör så att nya anslutningar inte kan bli till 
        self.running = False
        
        # Stänger alla klienters sockets 
        for client in Server.Clients:
            try:
                client['client_socket'].close()
            except Exception as e:
                print(f"Error closing connection for {client['client_name']}: {e}")
        
        # Väntar på att alla trådar slutar 
        for thread in self.threads:
            thread.join()
        
        # Stäng serverns socket 
        self.socket.close()
        print("Server has been shut down.")

    def turn_off_server(self):
                print("Turning off the server...")
                self.shutdown()

if __name__ == '__main__':
    server = Server('127.0.0.1', 443)
    server.listen()





