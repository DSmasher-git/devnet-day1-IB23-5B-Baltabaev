"""
Packet Tracer Internal Python Script — Activity 8.8.3 Part 6
Run this code INSIDE Packet Tracer Python environment.
Copy the console output to: artifacts/day5/pt/pt_internal_output.txt
"""

import urllib.request
import json

BASE_URL = "http://localhost:58000/api/v1"

# Step 1: Get service ticket
ticket_url = BASE_URL + "/ticket"
ticket_data = json.dumps({"username": "netadmin", "password": "Admin_1234!"}).encode()
req = urllib.request.Request(
    ticket_url,
    data=ticket_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    ticket_resp = json.loads(resp.read())

ticket = ticket_resp["response"]["serviceTicket"]
print("serviceTicket:", ticket)

# Step 2: GET network-device
dev_req = urllib.request.Request(
    BASE_URL + "/network-device",
    headers={"X-Auth-Token": ticket}
)
with urllib.request.urlopen(dev_req) as resp:
    devices = json.loads(resp.read())

print("\n--- Network Devices ---")
for d in devices.get("response", []):
    print(f"  hostname={d.get('hostname')}  ip={d.get('managementIpAddress')}  type={d.get('type')}")

# Step 3: GET host
host_req = urllib.request.Request(
    BASE_URL + "/host",
    headers={"X-Auth-Token": ticket}
)
with urllib.request.urlopen(host_req) as resp:
    hosts = json.loads(resp.read())

print("\n--- Hosts ---")
for h in hosts.get("response", []):
    print(f"  hostName={h.get('hostName')}  hostIp={h.get('hostIp')}  hostMac={h.get('hostMac')}")

print("\nDone.")
