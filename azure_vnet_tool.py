#import os
import subprocess
import json
import re

directory = subprocess.check_output("pwd", shell=True, text=True)
# Remove the /n at the end of the output
directory = directory[:-1]

# Pull VNET info with AZ
subprocess.check_output("az network vnet list > vnets.txt", shell=True, text=True)

# Open text file and prepare it as a list
f = open(directory + "/vnets.txt")
az_cmd_output_str = f.read()
az_cmd_output_list = json.loads(az_cmd_output_str)

# Print name of each VNET
for vnet in az_cmd_output_list:
    print(str(vnet["name"]))
    index = 0
    for peer in vnet["virtualNetworkPeerings"]:
        print("  peer: " + re.search(r"(?!.*\/).+", str(vnet["virtualNetworkPeerings"][index]["remoteVirtualNetwork"]["id"])).group(0))
