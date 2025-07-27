#import os
import subprocess
import json
import time

directory = subprocess.check_output("pwd", shell=True, text=True)
# Remove the /n at the end of the output
directory = directory[:-1]

# Pull VNET info with AZ
# v original command
#subprocess.check_output("az network vnet list > vnets.json", shell=True, text=True)
subprocess.check_output("az graph query -q 'resources' > vnets.json", shell=True, text=True)

# Open text file and prepare it as a list
f = open(directory + "/vnets.json")
az_cmd_output_str = f.read()
az_cmd_output_dict = json.loads(az_cmd_output_str)

az_cmd_output_list = az_cmd_output_dict["data"]
vnets = []

for entry in az_cmd_output_list:
    if "/providers/Microsoft.Network/virtualNetworks/" in entry["id"]:
        vnets.append((str(entry["name"])))

for vnet in vnets:
    print(vnet)

