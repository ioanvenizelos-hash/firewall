#!/bin/bash

echo "Generating configs..."
python main.py

for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ip a flush dev $interface; done
for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ifdown --force $interface; done
for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ip link delete $interface; done

echo "Adding Interfaces..."
cat /firewall/generated_from_j2/interfaces_vlan.txt > /etc/network/interfaces
for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}' | tail -n +2); do ifup $interface; done

mkdir -p /var/lib/dhcp
touch /var/lib/dhcp/dhcpd.leases
chmod 644 /var/lib/dhcp/dhcpd.leases

cp /firewall/generated_from_j2/dhcpd.conf /etc/dhcp/dhcpd.conf

echo "Providing DHCP..."
for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}' | tail -n +2); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done

echo "Applying Firewall Rules..."
nft -f /firewall/generated_from_j2/firewall_rules.txt 2>/dev/null || true


(
	while true; do
		sleep 30
    		python3 main.py
    		if [ /firewall/generated_from_j2/firewall_rules.txt -nt /tmp/last_firewall_rules ]; then
    			cp /firewall/generated_from_j2/firewall_rules.txt /tmp/last_firewall_rules
    			nft -f /firewall/generated_from_j2/firewall_rules.txt 2>/dev/null || true
    		fi
    		if [ /firewall/generated_from_j2/interfaces_vlan.txt -nt /tmp/last_interfaces ]; then
    			cp generated_from_j2/interfaces_vlan.txt /tmp/last_interfaces
    			pkill -f dhcpd 2>/dev/null
                for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ip a flush dev $interface; done
                for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ifdown --force $interface; done
                for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}'); do ip link delete $interface; done
				cat /firewall/generated_from_j2/interfaces_vlan.txt > /etc/network/interfaces
                for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}' | tail -n +2); do ifup $interface; done
				mkdir -p /var/lib/dhcp
                touch /var/lib/dhcp/dhcpd.leases
				chmod 644 /var/lib/dhcp/dhcpd.leases
				cp /firewall/generated_from_j2/dhcpd.conf /etc/dhcp/dhcpd.conf
                for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}' | tail -n +2); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done
		fi
		if [ /firewall/generated_from_j2/dhcpd.conf -nt /tmp/last_dhcpd.conf ]; then
			cp generated_from_j2/dhcpd.conf /tmp/last_dhcpd.conf
			pkill -f dhcpd 2>/dev/null
			for interface in $(cat generated_from_j2/interfaces_vlan.txt | grep eth1 | grep auto | awk '{print $2}' | tail -n +2); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done
		fi
 	done
) &

tail -f /dev/null