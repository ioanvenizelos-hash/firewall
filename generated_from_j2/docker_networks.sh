#!/bin/bash

docker network create -d macvlan --subnet=192.168.20.0/24 --gateway=192.168.20.254 -o parent=eth1.20 vlan20_net
docker network connect --ip 192.168.20.1 vlan20_net nf_firewarll

docker network create -d macvlan --subnet=192.168.10.0/24 --gateway=192.168.10.254 -o parent=eth1.10 vlan10_net
docker network connect --ip 192.168.10.1 vlan10_net nf_firewarll
