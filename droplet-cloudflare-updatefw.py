#!/usr/bin/env python3
import requests as requests
import ipaddress
from digitalocean import Manager, Firewall, InboundRule, Sources
from sys import exit
import os

CF_NETBLOCK_URLS = ['https://cloudflare.com/ips-v4', 'https://cloudflare.com/ips-v6']
CF_NETBLOCK_FILE = '/tmp/cf_netblocks.txt'
DIGO_TOKEN = '___your digitalocean token goes here___'
FW_NAME = "cloudflare"

# API nuance: any port value can be a single port, a string range of ports (i.e. '8080-9000'), or 'all'
FW_SERVICES = [
    [[80, 443], 'tcp']
]


def get_netblocks():
    """ get ipv4 and ipv6 addresses from Cloudflare """

    netblocks = []
    for ip_url in CF_NETBLOCK_URLS:
        response = requests.get(ip_url)
        response.raise_for_status()
        for netblock in response.text.splitlines():
            try:
                ipaddress.ip_network(netblock)
                netblocks.append(netblock)
            except ValueError:
                print("Invalid network: " + netblock)
                exit(1)

    return netblocks


def save_netblocks(netblocks):
    with open(CF_NETBLOCK_FILE, "w") as file:
        file.write('\n'.join(str(netblock) for netblock in netblocks))


def netblocks_have_changed(netblocks):
    if not os.path.exists(CF_NETBLOCK_FILE):
        return True

    with open(CF_NETBLOCK_FILE, "r") as file:
        saved_netblocks = file.read().splitlines()

    diffs = list(set(netblocks) - set(saved_netblocks)) + list(set(saved_netblocks) - set(netblocks))
    if diffs:
        print(f"Netblock changes: {diffs}")
        return True

    return False


def get_droplet_ids(manager):
    """ get IDs of droplets associated with this token """

    ids = []
    droplets = manager.get_all_droplets()
    for droplet in droplets:
        ids.append(droplet.id)

    return ids


def get_firewall(manager):
    """ retrieve a list of firewalls and return id with name matching FW_NAME constant """

    firewalls = manager.get_all_firewalls()
    for firewall in firewalls:
        if firewall.name == FW_NAME:
            return firewall


def create_inbound_rules(netblocks):
    """ create a firewall """

    rules = []
    for service_ports, service_protocol in FW_SERVICES:
        for service_port in service_ports:
            print(f"Creating rule for {str(service_port)} {service_protocol}")
            rule = InboundRule(ports=service_port, protocol=service_protocol,
                               sources=Sources(addresses=netblocks))
            rules.append(rule)

    return rules


def create_firewall(rules, ids):
    """ create a new firewall """
    firewall = Firewall(token=DIGO_TOKEN, name=FW_NAME, inbound_rules=rules,
                        outbound_rules=[], droplet_ids=ids)
    firewall.create()

    return firewall


# pull most recent IP list from Cloudflare
cf_netblocks = get_netblocks()

# check if there are any differences
if not netblocks_have_changed(cf_netblocks):
    print("No changes. Nothing to do!")
    exit(0)

# initialize Digital Ocean API manager
digo_manager = Manager(token=DIGO_TOKEN)

# Get droplet ids
droplet_ids = get_droplet_ids(digo_manager)

# Create firewall rules for Digital Ocean
firewall_rules = create_inbound_rules(cf_netblocks)
print(firewall_rules)

# Get current firewall, if applicable
digo_firewall = get_firewall(digo_manager)
if digo_firewall:
    # delete old firewall
    if digo_firewall.destroy():
        pass
    else:
        # if there was a problem deleting the old firewall then proceed no further
        print("Could not destroy firewall: " + digo_firewall.id)
        exit(1)

# create new firewall, associated with droplets
digo_firewall = create_firewall(firewall_rules, droplet_ids)
print("Created new firewall: " + digo_firewall.id)

# save latest netblocks for comparison
save_netblocks(cf_netblocks)
