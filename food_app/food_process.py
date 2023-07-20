from collections import namedtuple
from pathlib import Path
from typing import List
import os
import numpy as np
import pandas as pd

# Define the mapping of column types
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

# Structure holding reduced database
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

    return dataframes

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

def create_orders_by_meal_type_age_cuisine_table(db: MultiDimDatabase) -> pd.DataFrame:
    # Extracting required information from the tables
    orders_df = db.orders
    birthdates_df = db.birthdates
    food_df = db.food

    # Mapping meal types based on order time
    def get_meal_type(order_time):
        if 6 <= order_time.hour < 10:
            return 'breakfast'
        elif 10 <= order_time.hour <= 16:
            return 'lunch'
        else:
            return 'dinner'

    # Mapping user age groups based on birth year
    def get_user_age_group(year):
        if year >= 1995:
            return 'young'
        elif 1970 <= year < 1995:
            return 'adult'
        else:
            return 'old'

    # Adding columns 'meal_type' and 'user_age' to the orders_df
    orders_df['ordered_at'] = pd.to_datetime(orders_df['ordered_at'])  # Corrected column name
    orders_df['meal_type'] = orders_df['ordered_at'].apply(get_meal_type)
    orders_df['user_age'] = birthdates_df['year'].apply(get_user_age_group)  # Corrected column name

    # Merging orders_df with food_df to get 'food_cuisine'
    orders_by_meal_type_age_cuisine_df = orders_df.merge(food_df[['food_id', 'cuisine_id']], on='food_id', how='left')
    orders_by_meal_type_age_cuisine_df = orders_by_meal_type_age_cuisine_df[['order_id', 'meal_type', 'user_age', 'cuisine_id']]

    return orders_by_meal_type_age_cuisine_df.sort_values('order_id').reset_index(drop=True)











# Call the function to load and print the DataFrames
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

# Printing the original loaded data
for table_name, df in zip(TABLES, loaded_dataframes):
    print(f"Table: {table_name}")
    print(df)
    print("\n")

# Reducing the database
reduced_data = reduce_dims(db)
#
# Printing the reduced data
for table_name, df in reduced_data._asdict().items():
    print(f"Table: {table_name}")
    print(df)
    print("\n")

# Creating the orders_by_meal_type_age_cuisine table
orders_by_meal_type_age_cuisine_table = create_orders_by_meal_type_age_cuisine_table(db)

# Printing the orders_by_meal_type_age_cuisine table
print("Columns of the 'orders' DataFrame:")
print(loaded_dataframes[7].columns)
