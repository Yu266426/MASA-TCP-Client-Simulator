import asyncio

from message import HeartbeatMessage

HOST = "127.0.0.1"
PORT = 9999


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
	addr = writer.get_extra_info("peername")
	print(f"Connected by {addr}")

	while True:
		data: bytes = await reader.read(1024)
		if not data:
			break

		writer.write(bytes(HeartbeatMessage()))
		await writer.drain()

	print(f"Disconnected by {addr}")
	writer.close()
	await writer.wait_closed()


async def start_server():
	server = await asyncio.start_server(handle_client, HOST, PORT)

	async with server:
		await server.serve_forever()


asyncio.run(start_server())
