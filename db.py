import pyodbc

def update_table(server, database, username, password, table_name, column1_value, column2_value, column3_value, column4_value, column5_value, column6_value, column7_value, id_to_update):
    """
    Updates the specified columns in a SQL Server table based on the given ID.
    """
    # Define the SQL UPDATE statement to update multiple columns in the table
    update_query = f"UPDATE {table_name} SET column1 = ?, column2 = ?, column3 = ?, column4 = ?, column5 = ?, column6 = ?, column7 = ? WHERE id = ?"

    # Define the values for the parameters in the SQL statement
    new_values = (column1_value, column2_value, column3_value, column4_value, column5_value, column6_value, column7_value, id_to_update)

    # Establish a connection to the SQL Server database
    conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    try:
        # Execute the SQL UPDATE statement with the parameter values
        cursor.execute(update_query, new_values)

        # Commit the transaction after the update is done
        conn.commit()
    except:
        # Rollback the transaction if there is an error
        conn.rollback()
        raise
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
