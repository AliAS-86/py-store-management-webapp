import mysql.connector
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service_utils import utilities as utils
from service_utils import mysql_utils
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# Connect to server
def db_init(db_name):
    # Connect to the mysql server
    cnx = mysql_utils.connect_to_db()

   # check if database exist
    cmd = f"SHOW DATABASES LIKE '{db_name}'"
    result = mysql_utils.cursor_executer(cmd, cnx, return_type="fetchone")
    logger.info(result)
       

if __name__ == "__main__":
    db_name = "test_store_management"
    db_init(db_name)

        

    
