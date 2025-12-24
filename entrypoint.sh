#!/bin/bash

echo "Starting NF Firewall Container..."

#1. Generate templates 
echo "Generating configs..."
python main.py

#2. Clear previous state
for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//'); do ip a flush dev $interface; done 
for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//' | grep @); do ip link delete $interface; done

#3. Apply interfaces
echo "Adding Interfaces..."
cat /firewall/generated_from_j2/interfaces_vlan.txt > /etc/network/interfaces
ifup -a -v

#4. Setup DHCP
mkdir -p /var/lib/dhcp
touch /var/lib/dhcp/dhcpd.leases
chmod 644 /var/lib/dhcp/dhcpd.leases

cp /firewall/generated_from_j2/dhcpd.conf /etc/dhcp/dhcpd.conf

#5 Start DHCP on VLANs
echo "Providing DHCP..."
for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//;s/@.*//'); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done

#6. Apply firewall
echo "Applying Firewall Rules..."
nft -f /firewall/generated_from_j2/firewall_rules.txt 2>/dev/null || true


# 7. Watch for changes
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
    			for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//'); do ip a flush dev $interface; done 
			for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//' | grep @); do ip link delete $interface; done
			cat /firewall/generated_from_j2/interfaces_vlan.txt > /etc/network/interfaces
			ifup -a -v
			mkdir -p /var/lib/dhcp
			touch /var/lib/dhcp/dhcpd.leases
			chmod 644 /var/lib/dhcp/dhcpd.leases
			cp /firewall/generated_from_j2/dhcpd.conf /etc/dhcp/dhcpd.conf
			for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//;s/@.*//'); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done
		fi
		if [ /firewall/generated_from_j2/dhcpd.conf -nt /tmp/last_dhcpd.conf ]; then
			cp generated_from_j2/dhcpd.conf /tmp/last_dhcpd.conf
			pkill -f dhcpd 2>/dev/null
			for interface in $(ip a | grep 'eth1' | awk '{print $2}' | grep eth | sed 's/:$//;s/@.*//'); do dhcpd -4 -cf /etc/dhcp/dhcpd.conf -f $interface & done
		fi
 	done
) &

# Keep alive
tail -f /dev/null