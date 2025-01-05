import json
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# open the initial products json files into dictionaries so it can be pushed to the database
def json_loader(resource_path, repo_path=None):
    file_path = get_path(resource_path, repo_path=None)
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            # logger.info(data)
            return data
    except FileNotFoundError:
        logger.error(f"File not found in the provided file_path: {file_path}")

    except json.JSONDecodeError:
        logger.error("Error decoding the JSON file. Please check and validate the file's content")

def get_path(resource: str, repo_path: str = None) -> str:

    if repo_path is None:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    logger.info(repo_path)
    return os.path.join(repo_path, resource)
    
def get_dataset_schema(database, table, dataset):
    try:
        if "schema" not in dataset["datasets_to_tables"][f"table"] or not dataset["schemas"]:
            raise KeyError(f"Schema is not defined in the configuration file for {table}.")

        schema = dataset["schema"]
        logger.info("Schema loaded successfully:", schema)
    
    except KeyError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        (f"An unexpected error occurred: {e}")
        raise
        