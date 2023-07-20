import pytest
import pandas as pd
from food_app.food_process import load_tables, TABLES_DIR_PATH, TABLES

# Helper function to check if a DataFrame is empty
def is_empty_dataframe(df):
    return df.empty



# Test cases for load_tables function
@pytest.mark.parametrize("table_name", TABLES)
def test_load_tables(table_name):
    # Ensure that each table is loaded correctly
    dataframes = load_tables(TABLES_DIR_PATH, [table_name])
    assert len(dataframes) == 1
    assert isinstance(dataframes[0], pd.DataFrame)
    assert not is_empty_dataframe(dataframes[0])
