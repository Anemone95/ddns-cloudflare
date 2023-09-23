import requests
import json
import os
import subprocess
import re

def get_inet_value(interface_name):
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    pattern = rf'{interface_name}.*?inet (\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, output, re.DOTALL)

    if match:
        return match.group(1)
    else:
        raise Error("No ip address")

def get_public_ipv4():
    url = "http://169.254.169.254/latest/meta-data/public-ipv4"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        raise Error(f"Error fetching public IPv4: {e}")

zone_name = "anemone.top"
a_name = "mega.anemone.top"

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), 'r') as file:
    data = json.load(file)

# Extract 'email' and 'key' values
email = data['email']
key = data['key']
ip = get_public_ipv4()

headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": "wyxu95@gmail.com",
    "X-Auth-Key": "5ff4102a3b018b3ffd48fe545636dab21ad1c"
}
url = f"https://api.cloudflare.com/client/v4/zones?{zone_name}"

zones = requests.get(url, headers=headers).json()

if not zones['success']:
    raise Error("ERROR: "+zones)

for zone in zones["result"]:
    if zone["name"] == zone_name:
        zone_identifier = zone["id"]
        break

if not zone_identifier:
    raise Error("ERROR: zone name not exist")

dns_list_url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?name={a_name}"
dns_records = requests.get(dns_list_url, headers=headers).json()

if not dns_records['success']:
    raise Error("ERROR: "+dns_records)

if len(dns_records["result"]) == 0:
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records"
    data = {
        "content": ip,
        "name": "mega.anemone.top",
        "proxied": False,
        "type": "A",
        "comment": "DDNS record",
        "ttl": 1
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
else:
    id=dns_records["result"][0]['id']
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{id}"
    data = {
        "content": ip,
        "name": "mega.anemone.top",
        "proxied": False,
        "type": "A",
        "comment": "DDNS record",
        "ttl": 1
    }

    response = requests.put(url, headers=headers, json=data)

    print(response.text)
