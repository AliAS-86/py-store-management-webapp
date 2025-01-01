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

def connect_to_db():
    """A utility function to establish a connection to the mysql server and return a connection object"""
    try:    
        cnx = mysql.connector.connect(
            host = mysql_config["config"]["host"],
            port = mysql_config["config"]["port"],
            user = mysql_config["config"]["user"],
            password = mysql_config["config"]["password"]
        )
        logger.info("Database connection successful")
        return cnx
    
    except mysql.connector.Error as e:
        logger.error(f"MySQL Connection Error: {e}")
        return
    
def cursor_executer(cmd=None, query=None, values=None, curs_method=None, connection=None, return_type=None):
    """A method to execute mysql command and manage the cursor and/or connection (cnx) lifecycle"""
    cnx = connection
    logger.info(f"connection from cursor executer: {cnx}")
    close_connection = False
    if cnx is None:
        cnx = connect_to_db()
        close_connection = True
    try:
        with cnx.cursor() as cursor:
            if curs_method == "execute":
                cursor.execute(cmd)
                if return_type == "fetchall":
                    return cursor.fetchall()
                elif return_type == "fetchone":
                    return cursor.fetchone()
                elif return_type == "lastrowid":
                    return cursor.lastrowid
                elif return_type == "rowcount":
                    return cursor.rowcount
                return None
            elif curs_method == "executemany":
                cursor.executemany(query, values)
                cnx.commit()
                if return_type == "fetchall":
                    return cursor.fetchall()
                elif return_type == "fetchone":
                    return cursor.fetchone()
                elif return_type == "lastrowid":
                    return cursor.lastrowid
                elif return_type == "rowcount":
                    return cursor.rowcount
                return None
            

    finally:
        if close_connection:
            cnx.close()

        