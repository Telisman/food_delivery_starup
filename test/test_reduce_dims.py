import pytest
import pandas as pd
from food_app.food_process import MultiDimDatabase, ReducedDatabase, TYPE_MAPPING, reduce_dims

def test_reduce_dims():
    # Sample data for MultiDimDatabase
    data = {
        "addresses": pd.DataFrame({"address_id": [1, 2, 3], "district_id": [1, 2, 3], "street": ["A St", "B St", "C St"]}),
        "birthdates": pd.DataFrame({"birthdate_id": [1, 2, 3], "year": [1985, 1990, 1995], "month": [5, 3, 8], "day": [10, 15, 20]}),
        "cities": pd.DataFrame({"city_id": [1, 2, 3], "name": ["City A", "City B", "City C"], "state_id": [1, 2, 1]}),
        "countries": pd.DataFrame({"country_id": [1, 2], "name": ["Country X", "Country Y"]}),
        "cuisines": pd.DataFrame({"cuisine_id": [1, 2], "name": ["Cuisine A", "Cuisine B"]}),
        "districts": pd.DataFrame({"district_id": [1, 2, 3], "name": ["District X", "District Y", "District Z"], "city_id": [1, 2, 1]}),
        "food": pd.DataFrame({"food_id": [1, 2], "name": ["Food A", "Food B"], "cuisine_id": [1, 2], "price": [10.0, 15.0]}),
        "orders": pd.DataFrame({"order_id": [1, 2, 3], "user_id": [1, 2, 3], "address_id": [1, 2, 3], "food_id": [1, 2, 1]}),
        "promos": pd.DataFrame({"promo_id": [1, 2], "discount": [0.1, 0.2]}),
        "restaurants": pd.DataFrame({"restaurant_id": [1, 2], "name": ["Restaurant X", "Restaurant Y"], "address_id": [1, 2]}),
        "states": pd.DataFrame({"state_id": [1, 2], "name": ["State X", "State Y"], "country_id": [1, 2]}),
        "users": pd.DataFrame({"user_id": [1, 2, 3], "first_name": ["John", "Jane", "Jake"], "last_name": ["Doe", "Smith", "Johnson"], "birthdate_id": [1, 2, 3], "registered_at": ["2022-01-01", "2022-02-01", "2022-03-01"]}),
    }

    # Create a MultiDimDatabase instance with the sample data
    db = MultiDimDatabase(**data)

    # Call the reduce_dims function
    reduced_db = reduce_dims(db)

    # Check if the ReducedDatabase contains the expected tables
    assert set(reduced_db._fields) == {"orders", "users", "food", "promos", "restaurants", "addresses"}

    # Check if the types of columns are correctly mapped to the specified types in TYPE_MAPPING
    assert isinstance(reduced_db.orders, pd.DataFrame)
    assert isinstance(reduced_db.users, pd.DataFrame)
    assert isinstance(reduced_db.food, pd.DataFrame)
    assert isinstance(reduced_db.promos, pd.DataFrame)
    assert isinstance(reduced_db.restaurants, pd.DataFrame)
    assert isinstance(reduced_db.addresses, pd.DataFrame)

    for df in [reduced_db.orders, reduced_db.users, reduced_db.food, reduced_db.promos, reduced_db.restaurants, reduced_db.addresses]:
        for col, dtype in df.dtypes.items():
            assert dtype == TYPE_MAPPING[str(dtype)]

    # Check if the tables contain the correct number of rows
    assert len(reduced_db.orders) == 3
    assert len(reduced_db.users) == 3
    assert len(reduced_db.food) == 2
    assert len(reduced_db.promos) == 2
    assert len(reduced_db.restaurants) == 2
    assert len(reduced_db.addresses) == 3