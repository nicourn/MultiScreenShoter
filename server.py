import asyncio
import socket
import random

async def procesed_conn(num: int, sock:socket.socket, run_server:bool):
    loop = asyncio.get_event_loop()
    print(f"{num} started")
    while run_server:
        conn, arrd = await loop.sock_accept(sock)
        print(f"{arrd} connect")
        print(f"Start listing from {num}")
        while True:
            buff = await loop.sock_recv(conn, 1024)
            if b"break" in buff or len(buff) == 0:
                print(f"From {num} conn lost")
                break
            else:
                print(buff)
                # await get_img(conn, buff)


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


async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8090))
    listen = 2
    server.listen(listen)
    run_server = True
    try:
        await asyncio.gather(*(procesed_conn(i, server, run_server) for i in range(listen)))
    finally:
        server.close()


asyncio.run(main())



