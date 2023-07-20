import pytest
from food_app import food_process

# Test case for checking if the TYPE_MAPPING dictionary is defined
def test_type_mapping_defined():
    assert isinstance(food_process.TYPE_MAPPING, dict)

# Test case for checking if the TABLES list is defined
def test_tables_list_defined():
    assert isinstance(food_process.TABLES, list)

# Test case for checking if the TABLES_DIR_PATH variable is defined as a pathlib.Path object
def test_tables_dir_path_defined():
    assert isinstance(food_process.TABLES_DIR_PATH, food_process.Path)

# Test case for checking if the MultiDimDatabase namedtuple is defined correctly
def test_multi_dim_database_defined():
    assert hasattr(food_process, "MultiDimDatabase")
    assert isinstance(food_process.MultiDimDatabase, type)

# Test case for checking if the ReducedDatabase namedtuple is defined correctly
def test_reduced_database_defined():
    assert hasattr(food_process, "ReducedDatabase")
    assert isinstance(food_process.ReducedDatabase, type)

# Test case for checking if the load_tables function is defined
def test_load_tables_function_defined():
    assert hasattr(food_process, "load_tables")
    assert callable(food_process.load_tables)

# Test case for checking if the reduce_dims function is defined
def test_reduce_dims_function_defined():
    assert hasattr(food_process, "reduce_dims")
    assert callable(food_process.reduce_dims)

# Test case for checking if the create_orders_by_meal_type_age_cuisine_table function is defined
def test_create_orders_by_meal_type_age_cuisine_table_function_defined():
    assert hasattr(food_process, "create_orders_by_meal_type_age_cuisine_table")
    assert callable(food_process.create_orders_by_meal_type_age_cuisine_table)
