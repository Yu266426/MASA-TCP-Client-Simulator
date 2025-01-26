import asyncio
from typing import Literal

from message import create_random_message

HOST = "127.0.0.1"
PORT = 9999


async def client(board_id: Literal[0, 1, 2, 3], delay: float):
	reader, writer = await asyncio.open_connection(HOST, PORT)
	print(f"Board {board_id} connected")

	for _ in range(1000):
		writer.write(bytes(create_random_message(board_id)))
		await writer.drain()

		_data = await reader.read(1024)

		await asyncio.sleep(delay)

	writer.close()
	await writer.wait_closed()


async def main():
	clients = (
		client(1, 0.01),
		client(2, 0.01),
		client(3, 0.01),
	)

	await asyncio.gather(*clients)


asyncio.run(main())
