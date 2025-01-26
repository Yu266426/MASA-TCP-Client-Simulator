import random
import struct
from typing import Literal, Self


def create_random_message(board_id: Literal[0, 1, 2, 3]) -> "LimelightMessage":
	message_type = random.randrange(3)

	if message_type == 1:
		message = TelemetryMessage.random(board_id)
	if message_type == 2:
		message = ValveMessage.random()
	else:
		message = HeartbeatMessage()

	return message


class LimelightMessage:
	def __init__(self, header: int) -> None:
		self.header = header

	def __bytes__(self) -> bytes:
		output = self.header.to_bytes(1, byteorder="big")

		return output


class TelemetryMessage(LimelightMessage):
	FLIGHT_COMPUTER_NUM_VALUES = 47
	BAY_BOARD_NUM_VALUES = 52

	@classmethod
	def random(cls, board_id: Literal[0, 1, 2, 3]) -> Self:
		time_stamp = random.getrandbits(64)
		data = []

		if board_id == 0:
			num_values = cls.FLIGHT_COMPUTER_NUM_VALUES
		else:
			num_values = cls.BAY_BOARD_NUM_VALUES

		for _ in range(num_values):
			data.append(random.random())

		return cls(board_id, time_stamp, data)

	def __init__(self, board_id: Literal[0, 1, 2, 3], time_stamp: int, data: list[float]) -> None:
		if board_id == 0 and len(data) != self.FLIGHT_COMPUTER_NUM_VALUES:
			raise ValueError(
				f"Expected {self.FLIGHT_COMPUTER_NUM_VALUES} values in data for board_id {board_id}"
			)
		elif 0 < board_id and len(data) != self.BAY_BOARD_NUM_VALUES:
			raise ValueError(
				f"Expected {self.BAY_BOARD_NUM_VALUES} values in data for board_id {board_id}"
			)

		LimelightMessage.__init__(self, 0x01)

		self.board_id = board_id.to_bytes(1, byteorder="big")
		self.time_stamp = time_stamp.to_bytes(8, byteorder="big")
		self.data: list[float] = data

	def __bytes__(self) -> bytes:
		output = LimelightMessage.__bytes__(self)

		output += self.board_id
		output += self.time_stamp

		for data in self.data:
			output += struct.pack(">f", data)

		return output


class ValveMessage(LimelightMessage):
	@classmethod
	def random(cls) -> Self:
		command_bitmask = random.getrandbits(32)
		state_bitmask = random.getrandbits(32)

		return cls(command_bitmask, state_bitmask)

	def __init__(self, command_bitmask: int, state_bitmask: int) -> None:
		LimelightMessage.__init__(self, 0x02)

		self.command_bitmask = command_bitmask.to_bytes(4, byteorder="big")
		self.state_bitmask = state_bitmask.to_bytes(4, byteorder="big")

	def __bytes__(self) -> bytes:
		output = LimelightMessage.__bytes__(self)

		output += self.command_bitmask
		output += self.state_bitmask

		return output


class HeartbeatMessage(LimelightMessage):
	def __init__(self) -> None:
		LimelightMessage.__init__(self, 0x03)
