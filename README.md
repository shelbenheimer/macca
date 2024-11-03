# MACCA (MAC Spoofing Tool)
MACCA is a simple command-line MAC address spoofing tool. This tool operates using the built-in `ip` command in order to configure the MAC address of a particular network interface. By default, executing this tool will generate a random new MAC address using the **manuf.json** file that contains thousands of different OUI (organizationally unique identifiers) to disguise the device as something that it isn't. The last six bytes are then randomly generated using a built-in function.
# Application Usage
## Support:
Currently, this tool is only supported on **Linux** as it uses a method that is only available on **Linux**. Support for **Windows** is planned and will be implemented in future.
## Requirements:
- Scapy Library
- JSON Library
- RE (Regex) Library
```
python -m pip install ./requirements.txt
```
## Summary:
If for any reason your MAC address is important and must remain the same due to it being recognised by external / internal systems such as a whitelist on a network, **DO NOT** use this tool unless the prior address has been recorded. This tool can be used to bypass blacklists as I have tested it in such a scenario successfully. Using this tool for malicious / illegal reasons is something I **DO NOT** condone and doing so is at the risk of the user partaking in such activities.