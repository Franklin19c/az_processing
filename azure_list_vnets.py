#import os
import subprocess
import json

directory = subprocess.check_output("pwd", shell=True, text=True)
# Remove the /n at the end of the output
directory = directory[:-1]

# Pull VNET info with AZ
subprocess.check_output("az network vnet list > vnets.txt", shell=True, text=True)

# Open text file and prepare it as a list
f = open(directory + "/vnets.txt")
az_cmd_output_str = f.read()
az_cmd_output_list = json.loads(az_cmd_output_str)

vnets = []

for entry in az_cmd_output_list:
    vnets.append((str(entry["name"])))

for vnet in vnets:
    print(vnet)

