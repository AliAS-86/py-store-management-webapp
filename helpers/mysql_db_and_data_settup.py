import mysql.connector
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service_utils import utilities as utils
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# load mysql config from json file:
config_file_path = utils.get_path("config_files/db_config.json")
mysql_config = utils.json_loader(config_file_path)
# logger.info(mysql_config)


# Connect to server
def connect_to_db(db_name):
    try:
        cnx = mysql.connector.connect(
            host=mysql_config["config"]["host"],
            port=mysql_config["config"]["port"],
            user=mysql_config["config"]["user"],
            password=mysql_config["config"]["password"]
        )
        logger.info(cnx)
        cursor = cnx.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
        exists = cursor.fetchone() is not None

        cursor.close()
        cnx.close()

        return exists
    
    except mysql.connector.Error as e:
        logger.error(f"Error: {e}")
        return False
    
if __name__ == "__main__":
    db_name = "store_management"
    if connect_to_db(db_name):
        logger.info(f"Database {db_name} exists")
    else:
        logger.warning(f"Database {db_name} does not exist, run the db_creator function then retry to connect")

        

    
