from . import new_config
import config
from database import configs
from . import generate_server_config

conf = config.get_config()

def new_user_config(owner_id):
    new_conf = new_config.generate_new_config(conf["awg_dir"])
    new_conf_id = configs.insert_new_config(db=conf["db_filename"], free_ip=new_conf[0], public_key=new_conf[1], private_key=new_conf[2], owner_id=owner_id)
    generate_server_config.apply_new_conf(generate_server_config.generate_server_config())
    return new_conf_id
