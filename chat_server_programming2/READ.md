Kurs : Programmering 2 
Namn: Khilkhil Hossain 
Klass: Devops24 
Uppgift - Individuell socket chat-server

Mål = VG 

Kommentar: 

Hej Edvin , förlåt att uppgiften är sen. 
Fick meddelande från Alex att du inte haft tillgång till min git hub. Samt att jag till och med glömt att ladda upp den. Förlåt för detta ! 


1. Dessa är modulerna som krävs
```
import socket
from threading import Thread
import os

```
2. Detta är att starta serven , samt fel hantera om man startar filerna fel. 

```
if __name__ == '__main__':
    try:
        Client('127.0.0.1', 443) 
    except KeyboardInterrupt:
        print("\nExiting client program. Goodbye!")
        os._exit(0)

```

3. Fel-hantering om man råkar köra client.py först 

```
class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()# Detta skapar en ny socket per klient
        try:
            self.socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?") # Ifall man kör client filen först 
            os._exit(1)

```
