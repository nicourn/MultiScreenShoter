import asyncio
import socket

i = 0
SERVER_ADDRESS = ('192.168.0.101', 8090)
CONNECTIONS = 100

async def handle_client(client):
    global i

    while True:
        #request = (await loop.sock_recv(client, 255)).decode('utf8')
        #response = str(eval(request)) + '\n'
        #await loop.sock_sendall(client, response.encode('utf8'))

        l = await loop.sock_recv(client, 1024)
        if(l):
            f = open(f'{i}.png','wb')
            i = i + 1
            print("Получаем..")
            while (l):
		if b'end' in l:
		    break
                f.write(l)
                l = await loop.sock_recv(client, 1024)
            print("Скриншот получен")
            f.close()
	

    client.close()

async def run_server():
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen(CONNECTIONS)
server.setblocking(False)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_server())
