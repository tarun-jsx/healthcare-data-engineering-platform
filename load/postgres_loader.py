import pandas as pd



def load_dataframe(df, table_name, connection):
    """
    Load a Pandas DataFrame into a PostgreSQL table.
    """

    cursor = connection.cursor()

    try:
        # Convert DataFrame column names into a Python list
        columns = list(df.columns)

        # Join the column names into a comma-separated string
        columns_string = ", ".join(columns)

        # Create placeholders
        placeholders = ", ".join(["%s"] * len(columns))

        # Build INSERT query
        query = f"""
        INSERT INTO {table_name}
        ({columns_string})
        VALUES ({placeholders})
        """

        # Convert NumPy types and NaN to native Python types
        data = [
            tuple(
                None if pd.isna(value)
                else value.item() if hasattr(value, "item")
                else value
                for value in row
            )
            for row in df.to_numpy()
        ]

        # Insert all rows at once (Production Mode)
        cursor.executemany(query, data)

        # Commit changes
        connection.commit()

        print(f"Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        connection.rollback()
        print(f"Error loading table: {table_name}")
        print(e)

    finally:
        cursor.close()