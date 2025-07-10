# dashboard/utils.py

column_map = {
    "Transaction": {
        "count": "transaction_count",
        "amount": "transaction_amount",
        "category": "transaction_type"
    },
    "User": {
        "count": "registered_users",
        "amount": None,
        "percentage": None,
        "category": "brand"
    },
    "Insurance": {
        "count": "count",
        "amount": "amount",
        "percentage": None,
        "category": None  # No category in insurance table
    }
}

table_map = {
    "Transaction": "aggregated_transaction",
    "User": "aggregated_user",
    "Insurance": "aggregated_insurance"
}

district_table_map = {
    "Transaction": "map_transaction",
    "User": "map_user",
    "Insurance": "map_insurance"
}
