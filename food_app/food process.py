from collections import namedtuple
from pathlib import Path
from typing import List
import os
import numpy as np
import pandas as pd

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


loaded_dataframes = load_tables(TABLES_DIR_PATH, TABLES)

for table_name, df in zip(TABLES, loaded_dataframes):
    print(f"Table: {table_name}")
    print(df)
    print("\n")

