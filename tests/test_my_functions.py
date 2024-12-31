import pytest
import src.my_functions as my_functions
import logging

logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def test_add():
    assert my_functions.add(1, 2) == 3
    assert my_functions.add(0, 0) == 0
    assert my_functions.add(-1, -1) == -2

    logger.info("test_add passed")

# def test_subtract():
#     assert my_functions.subtract(1, 2) == -1
#     assert my_functions.subtract(0, 0) == 0
#     assert my_functions.subtract(-1, -1) == 0

#     logger.info("test_subtract passed") 

def test_multiply():
    assert my_functions.multiply(1, 2) == 2
    assert my_functions.multiply(0, 0) == 0
    assert my_functions.multiply(-1, -1) == 1

    logger.info("test_multiply passed")

def test_divide():
    assert my_functions.divide(1, 2) == 0.5
    assert my_functions.divide(0, 1) == 0
    assert my_functions.divide(-1, -1) == 1

    logger.info("test_divide passed")
