"""Shared, fail-closed lab-network membership check (stdlib only)."""
import ipaddress
import os
import sys


def on_lab_network(address, network=None):
    network = os.environ.get('RL_LAB_NETWORK', '') if network is None else network
    try:
        scope = ipaddress.ip_network(network, strict=True)
        host = ipaddress.ip_interface(address).ip
        return scope.version == host.version == 4 and host in scope
    except (ValueError, TypeError):
        return False


if __name__ == '__main__':
    if not os.environ.get('RL_LAB_NETWORK'):
        print('Set RL_LAB_NETWORK to the authorized lab IPv4 CIDR.', file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(0 if len(sys.argv) == 2 and on_lab_network(sys.argv[1]) else 1)
