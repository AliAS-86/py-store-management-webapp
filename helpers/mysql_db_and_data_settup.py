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
    # command to be executed by cursor_executer utility function to connect to the mySQL server and check if a db exist
    cmd = f"SHOW DATABASES LIKE '{db_name}';"
    result = mysql_utils.cursor_executer(cmd, connection=cnx, return_type="fetchone")
    logger.info(result)
    # results fetched from executing the query above shows data, and not None, meaning that db in question does exist
    if result is not None:
        logger.info(f"Database {db_name} exists")
        cmd_db_get_tables = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';"
        db_tables = mysql_utils.cursor_executer(cmd_db_get_tables, connection=cnx, return_type="fetchall")
        logger.info(db_tables)
        # iterate through the tables in databases and check if they have contents
        for table in db_tables:
            cmd_table_data = f"SELECT COUNT(*) FROM {db_name}.{table[0]};"
            db_table_content = mysql_utils.cursor_executer(cmd_table_data, return_type="fetchone")
            if db_table_content[0] > 0:
                logger.info(f"for database {db_name}, table {table}, the table is seeded with {db_table_content} of rows")
            elif db_table_content[0] == 0:
                logger.info(f"for database {db_name}, table {table}, the table is not seeded")
                user_input = input("Do you want to load the sample data provided in the resources directory (Yes/No): ")
                if user_input == "Yes":
                    db_data_load(cnx)
                # if user selected no, then no further actions to be taken
                else:
                    logger.info(f"Empty database initiated: {db_name}")

def db_data_load(cnx):
    groceries_seed_data_path = utils.get_path("resources/dataset_groceries.json")
    groceries_seed_data = utils.json_loader(groceries_seed_data_path)

    bulk_insert_query = "INSERT INTO groceries (product_id, name, description, original_price, discount_flag, discounted_price, quantity) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    values = [(
        item["prod_id"], 
        item["prod_name"], 
        item["prod_description"], 
        item["prod_price"],
        item["discounted_item"],
        item["prod_discounted_price"],
        item["prod_quantity"])
        for item in groceries_seed_data]
    executemany_results = mysql_utils.cursor_executer(query=bulk_insert_query, values=values, curs_method="executemany", connection=cnx, return_type="rowcount")
    logger.info(f"{executemany_results} rows inserted successfully to groceries table.")


if __name__ == "__main__":
    db_name = "store_management"
    db_init(db_name)

        

    
