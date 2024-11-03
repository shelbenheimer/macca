#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer)

from scapy.all import conf
from sys import argv
import random
import subprocess
import platform
import json
import re
import os

class Spoof:
	def __init__(self, mac, interface):
		self.mac = mac
		self.interface = interface

	def ValidateMAC(self):
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

	def ChangeMAC(self):
		if not self.ValidateMAC():
			print(f"Invalid MAC address {self.mac}.")
			return

		match platform.system():
			case 'Linux':
				subprocess.run(["ip", "link", "set", f"{self.interface}", "down"])
				subprocess.run(["ip", "link", "set", f"{self.interface}", "address", f"{self.mac}"])
				subprocess.run(["ip", "link", "set", f"{self.interface}", "up"])

				print(f"Attempting to change MAC ({self.mac}).")
				return True
			case 'Windows':
				print("This application does not currently support Windows.")
				return False

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
	return "{}:{}{}:{}{}:{}{}".format(
		GenRandOUI(vendors),
		GenRandByte(byte_range),
		GenRandByte(byte_range),
		GenRandByte(byte_range),
		GenRandByte(byte_range),
		GenRandByte(byte_range),
		GenRandByte(byte_range)
	).upper()

def ParseArgs(args, params):
	temp = params
	for arg in range(0, len(args)):
		match args[arg]:
			case '-m':
				temp["MAC"] = args[arg + 1]
			case '-i':
				temp["Interface"] = args[arg + 1]
	return temp

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/shelbenheimer)"
VENDOR_PATH = "Resources/manuf.json"

BYTE_RANGE = [
	[ 0, 1, 2, 3, 5, 6, 7, 8, 9 ],
	[ 'a', 'b', 'c', 'd', 'e', 'f' ]
]

try:
	print(BANNER)

	path = f"{os.path.dirname(os.path.abspath(__file__))}/{VENDOR_PATH}"
	vendors = PopulateList(path)

	params = { "MAC": GenRandMAC(vendors, BYTE_RANGE), "Interface": conf.iface }
	params = ParseArgs(argv, params)
	
	spoof = Spoof(params["MAC"], params["Interface"])
	spoof.ChangeMAC()
except KeyboardInterrupt:
	print("Caught interruption. Exiting gracefully.")