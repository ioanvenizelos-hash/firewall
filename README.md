# Containerized Firewall

Containerized firewall hosted on a Debian 12 server (Raspberry Pi) with two physical ethernet adapters.

## Stack

- Python 3.11, FastAPI, Uvicorn, Pydantic, Jinja2, psycopg2
- Docker & Docker Compose
- PostgreSQL 15
- nftables, ISC DHCP, VLANs on Linux, iproute2

## Architecture

**nf_firewall**  
- Python container with nftables, DHCP server, VLAN tooling and `main.py`.  
- Talks to the API containers, renders templates under `/firewall/templates/`, writes configs under `/firewall/generated_from_j2/`.  
- Entry script `/firewall/entrypoint.sh` runs `main.py`, generates configs and starts firewall services.

**firewall-api**  
- FastAPI service exposing `/firewall_rules` endpoints to list, create, edit and delete firewall rules stored in Postgres.

**interfaces-api**  
- FastAPI service exposing `/interfaces` REST API to manage VLAN/interface definitions.  
- Data is stored in the same Postgres database and used to build VLAN, DHCP and Docker network configs.

## Project structure

```text
.
├── ansible/                 # reserved for future automation
├── db/
│   ├── mydb_backup.sql      # example DB backup
│   └── postgres.env         # DB credentials (ignored in git)
├── docker-compose.yaml      # defines postgres, firewall-api, interfaces-api, nf_firewall
├── dockerfiles/
│   ├── firewall_api.Dockerfile
│   ├── interfaces_api.Dockerfile
│   └── nf_firewall.Dockerfile
├── src/
│   ├── main.py              # pulls data from APIs, renders Jinja2 templates
│   ├── firewall_api.py      # FastAPI app for firewall_rules table
│   └── interfaces_api.py    # FastAPI app for interfaces table
├── templates/
│   ├── dhcpd.conf.j2
│   ├── interfaces_vlan.j2
│   └── nf_firewall_rules_list.j2
├── entrypoint.sh            # orchestrates config generation and firewall startup
├── requirements.txt
└── .gitignore
