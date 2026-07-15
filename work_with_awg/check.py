import subprocess
import logging

logger = logging.getLogger(__name__)

def check_amnezia():
    try:
        result = subprocess.run(["awg"], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        logger.error("awg is not installed!")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"error while executing command\"awg\": {e}")
        return False
    except:
        logger.error("unknown error!")
        return False
    if result.stdout.startswith("interface: awg0"):
        return True
    return False