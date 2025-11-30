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


base_url="http://127.0.0.1:8000/firewall_rules/"

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



def create_template():
    env = Environment(loader=FileSystemLoader('/home/pi/firewall/templates/'))
    template = env.get_template("firewall_rules_list.j2")
    
    for firewall_rules in get_rules():
        if firewall_rules['enabled'] == True:
            parts = []
            parts.append("-A FORWARD")

            if firewall_rules.get("source"):
                parts.append(f"-s {firewall_rules['source']}")
            if firewall_rules.get("dest"):
                parts.append(f"-d {firewall_rules['dest']}")
            if firewall_rules.get("protocol"):
               parts.append(f"-p {firewall_rules['protocol']}")
            if firewall_rules.get("dest_port"):
                parts.append(f"--dport {firewall_rules['dest_port']}")
            if firewall_rules.get("action"):
                parts.append(f"-j {firewall_rules['action']}")

        rule_string = " ".join(parts)
        
        print(rule_string)

       


#    output = template.render(rules=rules)
#    print(output)

def main():
    create_template()
    
if __name__ == '__main__':
    main()
             