# DNS Zone Transfer (AXFR) Subdomain Enumerator
AXFR subdomain enumerator — small project from “DNS enumeration using Python” on Hack The Box Academy.

An educational command‑line tool for attempting DNS zone transfers (AXFR) against one or more authoritative nameservers, enumerating owner names from the zone, converting them to FQDNs, deduplicating them, and printing a sorted list with totals.

Use this in authorized environments only (labs, your own domains, or with explicit permission).

---

## Table of Contents

- Overview
- Features
- How It Works
- Requirements
- Installation
- Usage
- Output
- Examples
- Tips and Best Practices
- Troubleshooting
- FAQ
- Contributing
- License
- Disclaimer

---

## Overview

Zone transfers (AXFR) replicate entire DNS zones between nameservers. If enabled for untrusted clients, they can reveal subdomains at scale. This tool automates:
- Attempting AXFR against one or more nameservers
- Collecting owner names from the zone
- Converting them to FQDNs
- Deduplicating and printing sorted results with a total unique count

Note: Most production nameservers correctly refuse AXFR. Successful transfers typically indicate a lab setup or misconfiguration.

---

## Features

- Attempts AXFR per provided nameserver and continues on failures.
- Skips the zone apex “@” so the bare domain isn’t counted.
- Deduplicates results using a set for deterministic output.
- Sorted output with a final unique count.
- Simple, explicit CLI flags.
- Version flag for quick verification.

---

## How It Works

1. You provide:
   - A target domain (zone)
   - A comma‑separated list of nameservers (hostnames or IPs)
2. The tool attempts a full zone transfer (AXFR) from each nameserver over TCP/53.
3. For successful transfers, it iterates zone owner names, filters out “@”, builds FQDNs, and aggregates them into a unique set.
4. Prints a sorted list and total count.

---

## Requirements

- Python 3.8 or newer
- dnspython

---

## Installation

- System/global:
  - pip install dnspython
- Per‑user:
  - pip install --user dnspython
- Specific Python version:
  - python3.10 -m pip install dnspython

Optional:
- Create a virtual environment:
  - python3 -m venv .venv
  - source .venv/bin/activate  (Linux/macOS)
  - .\.venv\Scripts\activate   (Windows)
  - pip install dnspython

- Make it executable:
  - chmod +x dns_axfr_enum.py

---

## Usage

Basic syntax:
- python3 dns_axfr_enum.py -d <DOMAIN> -n <NS1,NS2,...>

Or:
- ./dns_axfr_enum.py -d <DOMAIN> -n <NS1,NS2,...>

Arguments:
- -d Domain (required)
  - Target zone (e.g., example.com)
- -n Nameserver(s) (required)
  - Comma‑separated authoritative nameservers (hostnames or IPs)
  - Examples: ns1.example.com,ns2.example.com or 192.0.2.53,198.51.100.12
- -v
  - Print version and exit

---

## Output

- On successful transfer from a nameserver:
  - [*] Successful Zone Transfer from <nameserver>
- Final results:
  - Sorted list of discovered FQDNs
  - -------- Total unique subdomains: <count>
- If all transfers fail or yield no entries:
  - No subdomains found.

Exit behavior:
- Missing required flags prints help and exits.
- No discoveries prints a message and exits.

---

## Examples

- Single nameserver by hostname:
  - python3 dns_axfr_enum.py -d inlanefreight.htb -n ns1.inlanefreight.htb
- Multiple nameservers:
  - python3 dns_axfr_enum.py -d example.com -n ns1.example.com,ns2.example.com
- Nameservers by IP:
  - python3 dns_axfr_enum.py -d example.com -n 192.0.2.53,198.51.100.12 

---

## Tips and Best Practices

- Ensure the nameservers are authoritative for the target domain.
- Using hostnames for nameservers requires your system DNS to resolve them.
- AXFR uses TCP/53; confirm connectivity and firewall rules.
- Use IP addresses for nameservers if resolution is flaky in your environment.
- For labs, verify AXFR is intentionally enabled.

---

## Troubleshooting

- Transfer refused or not authorized:
  - The server disallows AXFR. Try another authoritative server or verify lab configuration.
- Timeouts:
  - Check TCP/53 reachability, VPNs, or firewall rules.
- Empty results despite “Success”:
  - The zone may have few labels beyond the apex, or deduplication removed duplicates.
- Name resolution errors:
  - Use nameserver IPs directly, or fix local resolver configuration.

---

### Hack The Box VPN connectivity issues and verification

If AXFR requests time out, or it refuses to connect to the target nameserver, in HTB labs, ensure your VPN is up and routing lab traffic.

- Connect via CLI:
  - sudo openvpn --config /path/to/your.ovpn
  - If unstable, try a different .ovpn profile (switch VPN server or switch UDP/TCP)
    - Sometimes if you change the VPN Server, it will work.
- Connect via GUI:
  - Use the “OpenVPN Connect” app and import/select your .ovpn profile
    - On Kali Linux, to ensure the fastest connection, use the cli option.

After connecting or switching, verify:

- Interface and HTB IP assigned:
  - Linux/macOS: ip addr | grep -E "tun|tap|wg|inet "
  - Windows (PowerShell): Get-NetIPAddress | Where-Object {$_.InterfaceAlias -match 'TAP|TUN|WireGuard'}

- Reach the target nameserver:
  - Linux/macOS: ping -c 4 <NAMESERVER_IP>
  - Windows: ping <NAMESERVER_IP>

- Check TCP/53 to the nameserver:
  - Linux/macOS (netcat): nc -vz <NAMESERVER_IP> 53
  - Bash fallback: timeout 3 bash -c '</dev/tcp/<NAMESERVER_IP>/53' && echo "open" || echo "closed"
  - Windows (PowerShell): Test-NetConnection <NAMESERVER_IP> -Port 53

- Optional AXFR probe:
  - dig AXFR <DOMAIN> @<NAMESERVER_IP>
    - Example: dig AXFR inlanefreight.htb @10.129.184.83
    - If successful, you should see a list of subdomains.

If it still fails:
- Confirm the VPN shows connected and review OpenVPN logs.
- Cross‑check the same target using the Hack The Box web instance (in‑browser lab)

If the setup is correct, you should see a list of subdomains, without changing the /etc/hosts file.

---

## Contributing

- Open issues for bugs and feature requests.
- Submit PRs with clear descriptions.
- Keep output deterministic and CLI stable.

---

## Disclaimer

For educational and authorized testing only. Use responsibly and legally. The authors and contributors are not liable for misuse or damages.
