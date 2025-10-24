#!/usr/bin/env python3

# Dependencies:
# dnspython

# Import necessary modules
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

# Use a set to store unique subdomains
Subdomains = set()

# Define the AXFR Function
def AXFR(domain, nameserver):
    try:
        # Perform the zone transfer
        zone = dz.from_xfr(dq.xfr(nameserver, domain))

        if zone:
            print('[*] Successful Zone Transfer from {}'.format(nameserver))

            # Iterate owner names in the zone and build FQDNs, skipping apex "@"
            for name, node in zone.nodes.items():
                owner_rel = name.to_text()  # e.g., '@', 'www', 'dev'
                if owner_rel == '@':
                    continue
                fqdn = f'{owner_rel}.{domain}'.rstrip('.')
                Subdomains.add(fqdn)

    except Exception as error:
        print(error)
        pass

# Main
if __name__ == "__main__":

    # ArgParser - Define usage
    parser = argparse.ArgumentParser(
        prog="dns-axfr.py",
        epilog="DNS Zonetransfer Script",
        usage="dns-axfr.py [options] -d <DOMAIN>",
        prefix_chars='-',
        add_help=True
    )

    # Positional Arguments
    parser.add_argument('-d', action='store', metavar='Domain', type=str,
                        help='Target Domain.\tExample: inlanefreight.htb', required=True)
    parser.add_argument('-n', action='store', metavar='Nameserver', type=str,
                        help='Nameservers separated by a comma.\tExample: ns1.inlanefreight.htb,ns2.inlanefreight.htb')
    parser.add_argument('-v', action='version', version='DNS-AXFR - v1.1',
                        help='Prints the version of DNS-AXFR.py')

    # Assign given arguments
    args = parser.parse_args()

    # Validate
    if not args.d:
        print('[!] You must specify target Domain.\n')
        print(parser.print_help())
        exit()

    if not args.n:
        print('[!] You must specify target nameservers.\n')
        print(parser.print_help())
        exit()

    # Variables
    Domain = args.d
    NS.nameservers = list(args.n.split(","))

    # For each nameserver
    for nameserver in NS.nameservers:
        AXFR(Domain, nameserver)

    # Print the results
    if Subdomains:
        print('-------- Found Subdomains:')
        for subdomain in sorted(Subdomains):
            print(subdomain)
        print('-------- Total unique subdomains: {}'.format(len(Subdomains)))
    else:
        print('No subdomains found.')
        exit()
