import socket
from threading import Thread


class Server:
    # Skapar en gemensam lista över länkade klienter.
    Clients = [] # en tom lista, som man sparar länkade klienter

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT)) # Binder socket till en specifik värd och port
        self.socket.listen() # Lyssnar på flera länkade klienter. Om man skrev listen(5) så kan man ansluta 5 klienter till servern 
        print(f"Server started on {HOST}:{PORT}. Awaiting connections...")

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print(f"Connected to user at {address}")
            print(f"Currently connected clients: {len(Server.Clients)}")

            client_name = client_socket.recv(1024).decode().strip()
            client = {'client_name': client_name, 'client_socket': client_socket}

             # Skriver att en ny client är med chat servern, eller en existerande 
            self.broadcast_message(client_name, f"{client_name} has joined the chat!")
            Server.Clients.append(client)

            Thread(target=self.handle_new_client, args=(client,)).start()



    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            try:
                client_message = client_socket.recv(1024).decode().strip()
                if not client_message or client_message.lower() == f"{client_name}: bye": # .lower för att ta emot fler stiliseringar (Bye, bYe ect)
                    self.broadcast_message(client_name, f"{client_name} has left the chat.")
                    Server.Clients.remove(client)
                    client_socket.close()
                    break
                else:
                    self.broadcast_message(client_name, client_message)
            except Exception as e:
                print(f"Error with {client_name}: {e}")
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
        
        # Tar bort klienter som har ingen förbindelse till servern. 
        for client in disconnected_clients:
            Server.Clients.remove(client)



if __name__ == '__main__':
    # Statar servern på local värden och port 443
    server = Server('127.0.0.1', 443)
    server.listen()




