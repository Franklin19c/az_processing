#import os
import subprocess
import json
import re
import matplotlib.pyplot as plt
import networkx as nx

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

vnets_and_peerings = []

for entry in az_cmd_output_list:
    #print(type(entry))
    #print(entry)
    if "/providers/Microsoft.Network/virtualNetworks/" in entry["id"]:
        vnet_name = entry["name"]
        vnet_and_peerings = {vnet_name: []}
        
    # Clear index and peering list
    index = 0
    peerings = []
    
    properties = entry["properties"]
    
    if "/providers/Microsoft.Network/virtualNetworks/" in entry["id"]:
        index2 = 0
        for peer_properties in properties["virtualNetworkPeerings"]:
            # ".group(0)" is to remove unwanted formatting
            peerings.append(re.search(r"(?!.*\/).+", str(properties["virtualNetworkPeerings"][index2]["properties"]["remoteVirtualNetwork"]["id"])).group(0))
            index2 += 1
        vnet_and_peerings[entry["name"]] = peerings
        vnets_and_peerings.append(vnet_and_peerings)
        index += 1

"""
for a in vnets_and_peerings:
    for key,value in a.items():
        print(key)
        for b in value:
            print("  " + b)
"""

G = nx.Graph()
"""
G.add_edge("test", 2)
G.add_edge("test", 3)
G.add_edge("test", 5)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
"""
for a in vnets_and_peerings:
    for vnet_local,vnet_remote in a.items():
        for vnet_remote_x in vnet_remote:
            G.add_edge(vnet_local, vnet_remote_x)

# explicitly set positions
#pos = {"test": (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}
pos = {"vnet-west-01": (-1, -1), "vm-boinc-01-vnet": (-1, 0), "vm-compute-eastus-001-vnet": (-1, 1), "vnet-compute-eastus-001": (0, -1), "vnet-hub-eastus-001": (0, 0), "vm-boinc-west2us-001-vnet": (0, 1), "vnet-sub2-01": (1, -1)}

options = {
    "font_size": 5,
    "node_size": 1000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
}
nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()

