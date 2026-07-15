import os
import config
import logging
import subprocess
import ipaddress
import secrets

logger = logging.getLogger(__name__)

def calculate_ipv6_from_ipv4(ipv4: str) -> str:
    # vibecoded, sorry :(
    conf = config.get_config()

    ipv4_subnet = ipaddress.ip_network(conf["awg_subnet"], strict=False)
    ipv6_subnet = ipaddress.ip_network(conf["awg_subnet_v6"], strict=False)

    ipv4_addr = ipaddress.ip_address(ipv4)

    if ipv4_addr not in ipv4_subnet:
        logger.error("IPv4 address %s is outside IPv4 subnet %s", ipv4_addr, ipv4_subnet)
        raise ValueError(f"IPv4 address {ipv4_addr} is outside {ipv4_subnet}")

    host_bits = ipv4_subnet.max_prefixlen - ipv4_subnet.prefixlen
    host_mask = (1 << host_bits) - 1
    host_part = int(ipv4_addr) & host_mask

    ipv6_host_bits = ipv6_subnet.max_prefixlen - ipv6_subnet.prefixlen

    if host_bits > ipv6_host_bits:
        logger.error(
            "IPv4 host part has %s bits, but IPv6 subnet %s has only %s host bits",
            host_bits,
            ipv6_subnet,
            ipv6_host_bits,
        )
        raise ValueError(
            f"IPv4 host part has {host_bits} bits, but IPv6 subnet {ipv6_subnet} has only {ipv6_host_bits} host bits"
        )

    ipv6_addr = ipv6_subnet.network_address + host_part

    if ipv6_addr not in ipv6_subnet:
        logger.error("IPv6 address %s is outside IPv6 subnet %s", ipv6_addr, ipv6_subnet)
        raise ValueError(f"IPv6 address {ipv6_addr} is outside {ipv6_subnet}")

    return str(ipv6_addr)

def calculate_free_ip(awg_dir: str):
    if not os.path.exists(awg_dir + "/configs/.data.json"):
        ip = 2
        subnet = ipaddress.ip_network(config.get_config()["awg_subnet"], strict=False)
        result = subprocess.run(["awg"], capture_output=True, text=True, check=True).stdout
        for ip in subnet.hosts():
            if ip == subnet.network_address + 1: continue
            if not str(ip) in result:
                return str(ip)

def generate_new_config(awg_dir: str):
    os.makedirs(awg_dir + "/configs", exist_ok=True)
    free_ip = calculate_free_ip(awg_dir)
    random_string = secrets.token_hex(32)

    result = subprocess.run(
        f"awg genkey | tee /tmp/{random_string}_private.key | awg pubkey > /tmp/{random_string}_public.key",
        shell=True, capture_output=True, text=True, check=True)
    
    with open(f"/tmp/{random_string}_private.key", "r") as f:
        private_key = f.read()
    os.remove(f"/tmp/{random_string}_private.key")

    with open(f"/tmp/{random_string}_public.key", "r") as f:
        public_key = f.read()
    os.remove(f"/tmp/{random_string}_public.key")
    
    return free_ip, public_key, private_key