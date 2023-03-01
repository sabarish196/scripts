import pyodbc

def list_tables(server, database, username, password):
    """
    Retrieves a list of tables in the specified SQL Server database.
    """
    # Establish a connection to the SQL Server database
    conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    try:
        # Retrieve a list of tables in the database
        tables = [table.table_name for table in cursor.tables(tableType='TABLE')]

        # Print the list of tables
        print(f"The following tables are present in the {database} database:")
        print('\n'.join(tables))
    except:
        # Rollback the transaction if there is an error
        conn.rollback()
        raise
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
