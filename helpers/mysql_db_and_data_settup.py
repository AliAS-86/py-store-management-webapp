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
    cmd = f"SHOW DATABASES LIKE '{db_name}';"
    result = mysql_utils.cursor_executer(cmd, connection=cnx, return_type="fetchone")
    logger.info(result)
    if result is not None:
        logger.info(f"Database {db_name} exists")
        cmd_db_get_tables = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';"
        db_tables = mysql_utils.cursor_executer(cmd_db_get_tables, connection=cnx, return_type="fetchall")
        logger.info(db_tables)
        for table in db_tables:
            cmd_table_data = f"SELECT COUNT(*) FROM {db_name}.{table[0]};"
            db_table_content = mysql_utils.cursor_executer(cmd_table_data, return_type="fetchone")
            if db_table_content[0] > 0:
                logger.info(f"for database {db_name}, table {table}, the table is seeded with {db_table_content} of rows")
            elif db_table_content[0] == 0:
                logger.info(f"for database {db_name}, table {table}, the table is not seeded")
if __name__ == "__main__":
    db_name = "store_management"
    db_init(db_name)

        

    
