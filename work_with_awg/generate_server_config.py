from database import configs
import config
from work_with_awg.new_config import calculate_ipv6_from_ipv4
import subprocess

def generate_server_config():
    all_configs = configs.get_all_configs(config.get_config()["db_filename"])
    with open(config.get_config()["awg_dir"] + "/awg0.base.conf", "r") as f:
        awg_config = f.read().rstrip() + "\n\n"
    
    for conf in all_configs:
        if conf["status"] != "active":
            continue
        awg_config += f"""[Peer]
PublicKey = {conf["public_key"]}
AllowedIPs = {conf["ip"]}/32, {calculate_ipv6_from_ipv4(conf["ip"])}/128

"""
    return awg_config

def apply_new_conf(conf):
    with open(config.get_config()["awg_dir"] + "/awg0.conf", "w") as f:
        f.write(conf)
    awg_path = f"{config.get_config()['awg_dir']}/awg0.conf"
    subprocess.run(["bash", "-c", f"awg syncconf awg0 <(awg-quick strip {awg_path})", ], check=True,)
