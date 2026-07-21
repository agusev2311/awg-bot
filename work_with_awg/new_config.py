import os
import config
import logging
import subprocess
import ipaddress
import secrets
from database import configs

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
    del awg_dir
    conf = config.get_config()
    subnet = ipaddress.ip_network(conf["awg_subnet"], strict=False)
    used_ips = set()

    try:
        result = subprocess.run(["awg"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        result = ""

    for token in result.replace(",", " ").split():
        try:
            ip = ipaddress.ip_address(token.split("/")[0])
        except ValueError:
            continue
        if ip.version == 4 and ip in subnet:
            used_ips.add(str(ip))

    used_ips.update(configs.get_all_used_ips(conf["db_filename"]))

    for ip in subnet.hosts():
        if ip == subnet.network_address + 1:
            continue
        if str(ip) not in used_ips:
            return str(ip)

    raise RuntimeError("No free IP addresses available")

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
