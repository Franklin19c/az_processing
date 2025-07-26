#import os
import subprocess
import json
import re
#from tabulate import tabulate

directory = subprocess.check_output("pwd", shell=True, text=True)
# Remove the /n at the end of the output
directory = directory[:-1]

# Pull VNET info with AZ
subprocess.check_output("az network vnet list > vnets.json", shell=True, text=True)

# Open text file and prepare it as a list
f = open(directory + "/vnets.json")
az_cmd_output_str = f.read()
az_cmd_output_list = json.loads(az_cmd_output_str)

vnets_and_peerings = []

for entry in az_cmd_output_list:
    vnet_and_peerings = {}
    vnet_name = entry["name"]
    #print(vnet_and_peerings)
    
    index = 0
    peerings = []
    for peer in entry["virtualNetworkPeerings"]:
        peerings.append(re.search(r"(?!.*\/).+", str(entry["virtualNetworkPeerings"][index]["remoteVirtualNetwork"]["id"])).group(0))
        index += 1
    vnet_and_peerings[entry["name"]] = peerings
    vnets_and_peerings.append(vnet_and_peerings)

for a in vnets_and_peerings:
    for key,value in a.items():
        print(key)
        for b in value:
            print("  " + b)

