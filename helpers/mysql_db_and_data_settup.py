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
    result = mysql_utils.cursor_executer(cmd, curs_method="execute", connection=cnx, return_type="fetchone")
    logger.info(result)
    # results fetched from executing the query above shows data, and not None, meaning that db in question does exist
    if result is not None:
        logger.info(f"Database {db_name} exists")
        cmd_db_get_tables = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}';"
        db_tables = mysql_utils.cursor_executer(cmd_db_get_tables, curs_method="execute", connection=cnx, return_type="fetchall")
        logger.info(db_tables)
        # iterate through the tables in databases and check if they have contents
        for table in db_tables:
            # the cmd_db_get_tables return data in tuples. the table[index] will return the required element for the next command
            cmd_table_data = f"SELECT COUNT(*) FROM {db_name}.{table[0]};"
            db_table_content = mysql_utils.cursor_executer(cmd_table_data, curs_method="execute", return_type="fetchone")
            if db_table_content[0] > 0:
                logger.info(f"for database {db_name}, table {table[0]}, the table is seeded with {db_table_content} of rows")
            elif db_table_content[0] == 0:
                logger.info(f"for database {db_name}, table {table[0]}, the table is not seeded")
                user_input = input("Do you want to load the sample data provided in the resources directory (Yes/No): ").lower()
                if user_input == "yes":
                    db_data_load(cnx)
                # if user selected no, then no further actions to be taken
                else:
                    logger.info(f"Empty database initiated: {db_name}")

def db_data_load(cnx):
    """
    A function that take the dataset_table mapping from datasets_mapping json file and load the data to the tables if user want to initiate the table
    with some data for testing
    """
    datasets_to_tables_mapping_json = utils.json_loader("config_files/datasets_mapping_and_schema.json")
    logger.info(datasets_to_tables_mapping_json)
    for table, dataset_path in datasets_to_tables_mapping_json["datasets_to_tables"].items():
        database = datasets_to_tables_mapping_json["database"]
        dataset = utils.json_loader(dataset_path)
        user_input = input(f"You are about to seet {table} table with sample test data, you want to proceed? (Yes/No): ").lower()
        if user_input == "yes":
            schema_validation = mysql_utils.validate_schema(database, table, cnx, dataset)
            insert_results = mysql_utils.insert_data(database, table)
    # table_seed_data = 
    # groceries_seed_data_path = utils.get_path()
    # groceries_seed_data = utils.json_loader("resources/dataset_groceries.json")

    # electronics_seed_data_path = utils.get_path("resources/dataset_electronics.json")
    # electronics_seed_data = utils.json_loader(electronics_seed_data_path)

    # for file in data:
    #     bulk_insert_query = "INSERT INTO store_management.groceries (product_id, name, description, original_price, discount_flag, discounted_price, quantity) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    #     values = [(
    #         item["prod_id"], 
    #         item["prod_name"], 
    #         item["prod_description"], 
    #         item["prod_price"],
    #         item["discounted_item"],
    #         item["prod_discounted_price"],
    #         item["prod_quantity"])
    #         for item in file]
    #     executemany_results = mysql_utils.cursor_executer(query=bulk_insert_query, values=values, curs_method="executemany", connection=cnx, return_type="rowcount")
    #     logger.info(f"{executemany_results} rows inserted successfully to groceries table.")

    # bulk_insert_query = "INSERT INTO store_management.electronics (product_id, name, description, original_price, discount_flag, discounted_price, quantity) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    # values = [(
    #     item["prod_id"], 
    #     item["prod_name"], 
    #     item["prod_description"], 
    #     item["prod_price"],
    #     item["discounted_item"],
    #     item["prod_discounted_price"],
    #     item["prod_quantity"])
    #     for item in electronics_seed_data]
    # executemany_results = mysql_utils.cursor_executer(query=bulk_insert_query, values=values, curs_method="executemany", connection=cnx, return_type="rowcount")
    # logger.info(f"{executemany_results} rows inserted successfully to electronics table.")


if __name__ == "__main__":
    db_name = "store_management"
    cnx = mysql_utils.connect_to_db()
    db_data_load(cnx)