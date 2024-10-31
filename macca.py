#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer/ata-shell)

from scapy.all import conf
from json import load
from subprocess import run
from platform import system
from random import choice
import re
import os

class Spoof:
	def __init__(self, vendor_path, byte_range):
		self.vendor_path = vendor_path
		self.byte_range = byte_range

		self.mac = None
		self.interface = conf.iface

		self.platform = system()
		self.vendors = self.PopulateVendors(self.vendor_path)

	def ValidateMAC(self, address):
		valid = "FF:FF:FF:FF:FF:FF"
		if not len(address) == len(valid):
			return False

		pattern = r'^[0-9a-fA-F]$'
		for character in range(0, len(list(valid))):
			if valid[character] == ':': continue

			if not re.match(pattern, address[character]):
				return False
		return True

	def ChangeMAC(self, address):
		if not self.ValidateMAC(address):
			print(f"Invalid MAC address {address}.")
			return

		match self.platform:
			case 'Linux':
				run(["ip", "link", "set", f"{self.interface}", "down"], text=True)
				run(["ip", "link", "set", f"{self.interface}", "address", f"{address}"], text=True)
				run(["ip", "link", "set", f"{self.interface}", "up"], text=True)

				print(f"Changed MAC ({address}).")

	def PopulateVendors(self, path):
		with open(path, 'r', encoding='utf8') as file:
			return load(file)
		print("Failed to populate vendor list.")
		return {}

	def GenRandByte(self):
		random_byte = choice(self.byte_range)
		return choice(random_byte)

	def GenRandOUI(self):
		if not self.vendors: return
		return choice(list(self.vendors.keys()))

	def GenRandMAC(self):
		oui = self.GenRandOUI()
		return "{}:{}{}:{}{}:{}{}".format(
			oui,
			self.GenRandByte(),
			self.GenRandByte(),
			self.GenRandByte(),
			self.GenRandByte(),
			self.GenRandByte(),
			self.GenRandByte()
		).upper()

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/shelbenheimer/ata-shell)"
VENDOR_PATH = "Resources/manuf.json"
BYTE_RANGE = [
	[ 0, 1, 2, 3, 5, 6, 7, 8, 9 ],
	[ 'a', 'b', 'c', 'd', 'e', 'f' ]
]

try:
	path = f"{os.path.dirname(os.path.abspath(__file__))}/{VENDOR_PATH}"

	print(BANNER)
	spoof = Spoof(path, BYTE_RANGE)
	spoof.ChangeMAC(spoof.GenRandMAC())
except KeyboardInterrupt:
	print("Caught interruption. Exiting gracefully.")