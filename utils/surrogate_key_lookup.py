import psycopg2


def lookup_surrogate_key(
    conn,
    table_name,
    key_column,
    lookup_columns,
    lookup_values
):
    """
    Look up an existing surrogate key from a dimension table.
    Raises an error if no matching record is found.
    """

    cursor = conn.cursor()

    where_clause = " AND ".join(
        [f"{col} = %s" for col in lookup_columns]
    )

    query = f"""
        SELECT {key_column}
        FROM {table_name}
        WHERE {where_clause}
    """

    cursor.execute(query, lookup_values)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]

    raise ValueError(
        f"No matching record found in {table_name} "
        f"for {lookup_values}"
    )