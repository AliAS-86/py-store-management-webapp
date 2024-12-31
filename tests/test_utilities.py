# this pytest script to test the utilities scripts located in ../service_utils
import pytest
import logging
import os
from service_utils import utilities as utils

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# file_path = utils.get_path("config_files/fake_for_tests.json")
# logger.info(f"file path: {file_path}")

def test_json_loader():
    test_file_path = utils.get_path("config_files/fake_for_tests.json")
    data = utils.json_loader(test_file_path)
    logger.info(data)
    assert data["config"]["response"] == "data loading ok"