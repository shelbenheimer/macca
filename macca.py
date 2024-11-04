#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer)

import socket
import struct
import fcntl
import random
import platform
import json
import re
import os
import sys

SIOCSIFHWADDR = 0x8924
ARPHRD_ETHER = 1

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/shelbenheimer)"
VENDOR_PATH = "Resources/manuf.json"
DEFAULT_IFACE = "wlan0"

BYTE_RANGE = [
	[ 0, 1, 2, 3, 5, 6, 7, 8, 9 ],
	[ 'a', 'b', 'c', 'd', 'e', 'f' ]
]

class Spoof:
	def __init__(self, mac, interface):
		self.mac = str(mac)
		self.interface = str(interface)

	def ValidateMAC(self) -> bool:
		valid = "FF:FF:FF:FF:FF:FF"
		if not len(self.mac) == len(valid):
			return False

		pattern = r'^[0-9a-fA-F]$'
		for character in range(0, len(list(valid))):
			if valid[character] == ':':
				continue
			if not re.match(pattern, self.mac[character]):
				return False
		return True

	def ChangeMAC(self) -> bool:
		if not self.ValidateMAC():
			print(f"Invalid MAC address {self.mac}.")
			return

		if not platform.system() == "Linux":
			return False
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		mac_bytes = bytes.fromhex(self.mac.replace(":", ""))

		ifreq = struct.pack(
			'16sH6s8s',
			self.interface.encode('utf-8'),
			ARPHRD_ETHER,
			mac_bytes,
			b'\x00' * 8
		)

		try:
			fcntl.ioctl(sock.fileno(), SIOCSIFHWADDR, ifreq)
			return True
		except Exception as error:
			print(error)
			return False
		finally:
			sock.close()

def PopulateList(path):
	with open(path, 'r', encoding='utf8') as file:
		return json.load(file)
	print("Failed to populate list.")
	return None

def GenRandByte(byte_range):
	return random.choice(random.choice(byte_range))

def GenRandOUI(vendors):
	return random.choice(list(vendors.keys()))

def GenRandMAC(vendors, byte_range):
	remaining = 3
	temp = [ GenRandOUI(vendors) ]
	for iteration in range(0, remaining):
		temp.append(f"{GenRandByte(byte_range)}{GenRandByte(byte_range)}")
	return ":".join(temp).upper()

def ParseArgs(args, params):
	temp = params
	for arg in range(0, len(args)):
		match args[arg]:
			case '-m':
				temp["MAC"] = args[arg + 1]
			case '-i':
				temp["Interface"] = args[arg + 1]
	return temp

try:
	print(BANNER)

	path = f"{os.path.dirname(os.path.abspath(__file__))}/{VENDOR_PATH}"
	vendors = PopulateList(path)

	params = { "MAC": GenRandMAC(vendors, BYTE_RANGE), "Interface": DEFAULT_IFACE }
	params = ParseArgs(sys.argv, params)
	
	spoof = Spoof(params["MAC"], params["Interface"])

	if not spoof.ChangeMAC():
		sys.exit()

	print(f"Successfully changed MAC to {spoof.mac}")
except KeyboardInterrupt:
	print("Caught interruption. Exiting gracefully.")