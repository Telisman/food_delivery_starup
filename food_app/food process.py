from collections import namedtuple
from pathlib import Path
from typing import List
import os
import numpy as np
import pandas as pd


TYPE_MAPPING = {
    'int64': np.int64,
    'int32': np.int32,
    'int16': np.int16,
    'int8': np.int8,
    'uint64': np.uint64,
    'uint32': np.uint32,
    'uint16': np.uint16,
    'uint8': np.uint8,
    'float64': np.float64,
    'float32': np.float32,
    'object': object,
    'datetime64[ns]': np.datetime64,
}


# List of all tables used in the original database
TABLES = [
    "addresses",
    "birthdates",
    "cities",
    "countries",
    "cuisines",
    "districts",
    "food",
    "orders",
    "promos",
    "restaurants",
    "states",
    "users",
]

# Path to the directory where tables' CSV files are stored
TABLES_DIR_PATH = Path(__file__).parent / "tables"

# Structure holding initial database
MultiDimDatabase = namedtuple(
    "MultiDimDatabase",
    [
        "addresses",
        "birthdates",
        "cities",
        "countries",
        "cuisines",
        "districts",
        "food",
        "orders",
        "promos",
        "restaurants",
        "states",
        "users",
    ],
)
ReducedDatabase = namedtuple(
    "ReducedDatabase",
    [
        "orders",
        "users",
        "food",
        "promos",
        "restaurants",
        "addresses",
    ],
)

# --- Task #1 ---
def load_tables(tables_dir_path: Path, tables: List[str]) -> List[pd.DataFrame]:
    dataframes = []
    for table in tables:
        file_path = tables_dir_path / f"{table}.csv"
        df = pd.read_csv(file_path)

        # Get the file name without the .csv extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Check if 'id' column is present in the DataFrame
        if 'id' not in df.columns:
            # If 'id' column is missing, add it and populate with unique values
            df.insert(0, 'id', range(1, len(df) + 1))

        df.set_index("id", inplace=True)
        # print(df)  # Print the DataFrame
        # print(ReducedDatabase)

        dataframes.append(df)

    return dataframes# Call the function to load and print the DataFrames


def reduce_dims(db: MultiDimDatabase) -> ReducedDatabase:
    reduced_db = {}
    allowed_tables = ["orders", "users", "food", "promos", "restaurants", "addresses"]

    for table_name in allowed_tables:
        if hasattr(db, table_name):
            df = getattr(db, table_name)
            reduced_df = df.copy()
            reduced_df = reduced_df.astype({col: TYPE_MAPPING[str(col_type)] for col, col_type in df.dtypes.items()})
            reduced_db[table_name] = reduced_df

    return ReducedDatabase(**reduced_db)

loaded_dataframes = load_tables(TABLES_DIR_PATH, TABLES)

# Create a MultiDimDatabase instance with the loaded DataFrames
db = MultiDimDatabase(
    addresses=loaded_dataframes[0],
    birthdates=loaded_dataframes[1],
    cities=loaded_dataframes[2],
    countries=loaded_dataframes[3],
    cuisines=loaded_dataframes[4],
    districts=loaded_dataframes[5],
    food=loaded_dataframes[6],
    orders=loaded_dataframes[7],
    promos=loaded_dataframes[8],
    restaurants=loaded_dataframes[9],
    states=loaded_dataframes[10],
    users=loaded_dataframes[11],
)

# Reducing the database
reduced_data = reduce_dims(db)

# Printing the reduced data
for table_name, df in reduced_data._asdict().items():
    print(f"Table: {table_name}")
    print(df)
    print("\n")

loaded_dataframes = load_tables(TABLES_DIR_PATH, TABLES)

for table_name, df in zip(TABLES, loaded_dataframes):
    print(f"Table: {table_name}")
    print(df)
    print("\n")

