import pytest
import numpy as np
import pandas as pd
from datetime import datetime
from food_app.food_process import create_orders_by_meal_type_age_cuisine_table,MultiDimDatabase

# Sample data for testing
orders_data = {
    'order_id': [1, 2, 3],
    'user_id': [1, 2, 3],
    'address_id': [1, 2, 3],
    'restaurant_id': [1, 2, 3],
    'food_id': [1, 2, 3],
    'ordered_at': ['2020-02-12 14:04:04', '2020-03-31 09:15:25', '2020-04-28 23:54:08'],
    'promo_id': [np.nan, 'FRIES10OFF', np.nan],
}

birthdates_data = {
    'birthdate_id': [1, 2, 3],
    'year': [1986, 1992, 1998],
    'month': [12, 3, 10],
    'day': [18, 8, 5],
}

food_data = {
    'food_id': [1, 2, 3],
    'name': ['Tiny Mac', 'Fries', 'Pad Thai'],
    'cuisine_id': [4, 4, 7],
    'price': [20.0, 13.0, 25.0],
}

# Create DataFrames from the sample data
orders_df = pd.DataFrame(orders_data)
birthdates_df = pd.DataFrame(birthdates_data)
food_df = pd.DataFrame(food_data)

# Create a MultiDimDatabase instance with the sample DataFrames
test_db = MultiDimDatabase(
    addresses=None,  # Fill this with actual data if needed
    birthdates=birthdates_df,
    cities=None,  # Fill this with actual data if needed
    countries=None,  # Fill this with actual data if needed
    cuisines=None,  # Fill this with actual data if needed
    districts=None,  # Fill this with actual data if needed
    food=food_df,
    orders=orders_df,
    promos=None,  # Fill this with actual data if needed
    restaurants=None,  # Fill this with actual data if needed
    states=None,  # Fill this with actual data if needed
    users=None,  # Fill this with actual data if needed
)

# Define the test function using the pytest decorator
def test_create_orders_by_meal_type_age_cuisine_table():
    # Call the function to create the orders_by_meal_type_age_cuisine table
    orders_by_meal_type_age_cuisine_df = create_orders_by_meal_type_age_cuisine_table(test_db)

    # Assert the correctness of the result using specific test data or assertions
    assert isinstance(orders_by_meal_type_age_cuisine_df, pd.DataFrame)
    assert len(orders_by_meal_type_age_cuisine_df) == 3  # Replace 3 with the expected number of rows
    assert "order_id" in orders_by_meal_type_age_cuisine_df.columns
    assert "meal_type" in orders_by_meal_type_age_cuisine_df.columns
    assert "user_age" in orders_by_meal_type_age_cuisine_df.columns
    assert "cuisine_id" in orders_by_meal_type_age_cuisine_df.columns

    # You can add more assertions based on your specific requirements and expected output.

# Run the test with pytest
# In the terminal, navigate to the directory containing the test_food_process.py file and run:
# pytest test_food_process.py
