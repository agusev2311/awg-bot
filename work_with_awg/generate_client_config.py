from database.configs import get_config_by_id
from config import get_config
from . import new_config

def generate(config_id: int):
    conf = get_config_by_id(get_config()["db_filename"], config_id)

    with open(get_config()["awg_dir"] + "/client.base.conf", "r") as f:
        client_config = f.read()
        client_config = client_config.replace("{private_key}", conf["private_key"])
        client_config = client_config.replace("{free_ip}", conf["ip"])
        client_config = client_config.replace("{calculate_ipv6_from_ipv4(free_ip)}", new_config.calculate_ipv6_from_ipv4(conf["ip"]))
        client_config = client_config.replace("{public_key}", get_config()["awg_public"]) # server public!
        client_config = client_config.replace("{conf[\"awg_endpoint\"]}", get_config()["awg_endpoint"])
    
    return client_config