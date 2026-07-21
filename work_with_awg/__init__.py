from . import new_config
import config
from database import configs
from . import generate_server_config

conf = config.get_config()

def config_reload():
    generate_server_config.apply_new_conf(generate_server_config.generate_server_config())

def new_user_config(owner_id, name: str):
    new_conf = new_config.generate_new_config(conf["awg_dir"])
    new_conf_id = configs.insert_new_config(
        db=conf["db_filename"],
        free_ip=new_conf[0],
        public_key=new_conf[1],
        private_key=new_conf[2],
        owner_id=owner_id,
        name=name,
    )
    config_reload()
    return new_conf_id

def set_config_status(config_id: int, status: str):
    configs.update_config_status(conf["db_filename"], config_id, status)
    config_reload()

def delete_user_config(config_id: int):
    configs.delete_config(conf["db_filename"], config_id)
    config_reload()
