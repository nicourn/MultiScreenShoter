import asyncio
import socket
import random

async def get_new_connects(sock: socket.socket):
    loop = asyncio.get_event_loop()
    while True:
        conn, addr = await loop.sock_accept(sock)
        print(f"{addr} connected")
        await data_waiting(conn)


async def data_waiting(conn: socket.socket):
    loop = asyncio.get_event_loop()
    while conn:
        buff = await loop.sock_recv(conn, 1024)
        if not len(buff):
            print("No signal")
            await asyncio.sleep(0.5)
        else:
            print(len(buff))
            print("Yes signal")
            await get_img(conn, buff)


async def get_img(conn, arr):
    name = random.randint(1, 1000)
    loop = asyncio.get_event_loop()
    img = b""
    img += arr
    while b"end" not in arr:
        arr = await loop.sock_recv(conn, 1024)
        img += arr


    with open(f"{name}.png", "wb") as file:
        file.write(img)
        print(f"Write {name} = {len(img)}")



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8090))
sock.listen(10)
print("Start server")
try:
    asyncio.run(get_new_connects(sock))
except Exception as e:
    print(e)
finally:
    sock.close()
    print("Server close")
