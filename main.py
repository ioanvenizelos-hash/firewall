#!/usr/bin/env python3
import subprocess
import argparse
import ast
#import paramiko
import requests
import psycopg2
from datetime import datetime, timezone
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from jinja2 import Environment, FileSystemLoader


base_url="http://169.254.100.11:8000/firewall_rules/"

interfaces_url = "http://169.254.100.13:8001/interfaces/"


def get_rules(id = None,
    enabled = None,
    action = None,
    chain = None,
    source = None,
    source_port = None,
    dest = None,
    dest_port = None,
    protocol = None,
    description = None,
    order_index = None,
    user_defined = None,
    visible = None,
    group_id = None,
    extra = None) :

    url = f"{base_url}rules?"

    params = {
        "id": id,
        "enabled": enabled,
        "action": action,
        "chain": chain,
        "source": source,
        "source_port": source_port,
        "dest": dest,
        "dest_port": dest_port,
        "protocol": protocol,
        "description": description,
        "order_index": order_index,
        "user_defined": user_defined,
        "visible": visible,
        "group_id": group_id,
        "extra": extra,
    }

    for key, value in params.items():
        if value is not None:
            url += f"{key}={value}&"

    response = requests.get(url, verify=False)

    out = response.json().get("firewall", [])
    return(out)

def delete_rules(alert_id):
    url = f"{base_url}delete/{alert_id}"
    print(url)
    response = requests.delete(f"{url}", verify=False)
    if response.status_code == 200:
        print(f"Alert ID {alert_id} is deleted")
    elif response.status_code == 404:
         print(f"Alert ID {alert_id} is not found")
    else:
        print(f"Failed to delete alert {alert_id}. Status: {response.status_code}, Detail: {response.text}")

def get_interfaces(id = None,
    enabled = None,
    vlan_id = None,
    ip_address = None,
    interface_netmask = None,
    network = None,
    network_start = None,
    network_finish = None,
    gw = None,
    ) :

<<<<<<< HEAD
    url = f"{interfaces_url}?"
=======
    url = f"{interfaces_url}rules?"
>>>>>>> personal/main

    params = {
        "id": id,
        "enabled": enabled,
        "vlan_id": vlan_id,
        "ip_address": ip_address,
        "interface_netmask": interface_netmask,
        "network": network,
        "network_start": network_start,
        "network_finish": network_finish,
<<<<<<< HEAD
        "gw": gw
=======
        "gw": gw,
        "created_at": created_at,
        "updated_at": updated_at
>>>>>>> personal/main
    }

    for key, value in params.items():
        if value is not None:
            url += f"{key}={value}&"

    response = requests.get(url, verify=False)

    out = response.json().get("interfaces", [])
    return(out)



def create_fw_rules_template():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("nf_firewall_rules_list.j2")
    nf_rules = []
    for firewall_rules in get_rules():
        if firewall_rules['enabled'] == True:
            parts = []

            if firewall_rules.get("description"):
                parts.append(f"# {firewall_rules['description']}\n")
            if firewall_rules.get("source"):
                parts.append(f"\t\tip saddr {firewall_rules['source']}")
            if firewall_rules.get("dest"):
                parts.append(f"ip daddr {firewall_rules['dest']}")
            
            if firewall_rules.get("protocol"):
                if f"{firewall_rules['protocol'].lower()}" == 'icmp':
                    parts.append(f"ip protocol {firewall_rules['protocol'].lower()}")
                else:
                   parts.append(f"{firewall_rules['protocol'].lower()}")

            if firewall_rules.get("dest_port"):
                parts.append(f"dport {firewall_rules['dest_port']}")
            if firewall_rules.get("action"):
                parts.append(f"{firewall_rules['action']}".lower())

        rule_string = " ".join(parts)
              
        nf_rules.append(rule_string)

    output = template.render(forward_rules=nf_rules)
    with open("/firewall/generated_from_j2/firewall_rules.txt","w") as f:
<<<<<<< HEAD
        f.write(output)


def create_interfaces_template():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("interfaces_vlan.j2")

    ifaces = []

    for inter in get_interfaces():
        if inter['enabled'] == True:
            ifaces.append(inter)
        
    output = template.render(interfaces=ifaces)

    with open("/firewall/generated_from_j2/interfaces_vlan.txt","w") as f:
        f.write(output)

def create_dhcp_conf():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("dhcpd.conf.j2")
    dhcp_s =[]

    for dhcp in get_interfaces():
        if dhcp['enabled'] == True:
            dhcp_s.append(dhcp)

    output = template.render(networks=dhcp_s)
    with open("/firewall/generated_from_j2/dhcpd.conf","w") as f:
        f.write(output)

def create_docker_networks():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("docker_networks.sh.j2")
    dock_ns =[]

    for dock in get_interfaces():
        if dock['enabled'] == True:
            dock_ns.append(dock)

    output = template.render(dock_nets=dock_ns)
    with open("/firewall/generated_from_j2/docker_networks.sh","w") as f:
=======
>>>>>>> personal/main
        f.write(output)

def create_interfaces_template():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("interfaces_vlan.j2")

    ifaces = []

    for inter in get_interfaces():
        print(inter)
'''''
    data = {
    "interfaces": [
        {
            "vlan_id": 20,
            "ip_address": "192.168.20.1",
            "net_mask": "255.255.255.0"
        }
    ]
                }
'''''


#    output = template.render(**data)

#    with open("/firewall/generated_from_j2/interfaces_vlan.txt","w") as f:
#        f.write(output)


def create_dhcp_conf():
    env = Environment(loader=FileSystemLoader('/firewall/templates/'))
    template = env.get_template("dhcpd.conf.j2")

    data ={
        "networks":[
            {
                "network" : "192.168.20.0",
                "netmask" : "255.255.255.0",
                "network_start" : "192.168.20.100",
                "network_finish": "192.168.20.200",
                "gw" : "192.168.20.254"
            }

        ]
    }


    output = template.render(**data)
    with open("/firewall/generated_from_j2/dhcpd.conf","w") as f:
        f.write(output)


def main():
    create_interfaces_template()
    create_dhcp_conf()
    create_fw_rules_template()
<<<<<<< HEAD
    create_docker_networks()
=======
>>>>>>> personal/main

if __name__ == '__main__':
    main()
             