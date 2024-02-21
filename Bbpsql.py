import psycopg2

def insert_dict_to_psql(password, dbname='default_db', user='default_user', host='localhost', port='5432', table_name='default_table', data_dict={}):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['%s'] * len(data_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, list(data_dict.values()))
        
        conn.commit()
        print("Data inserted successfully!")
        
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")

# Example usage:
if __name__ == "__main__":
    password = 'your_password'
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    insert_dict_to_psql(password, table_name='your_table_name', data_dict=data)




import json
import psycopg2

def insert_dicts_from_file(password, filepath, dbname='default_db', user='default_user', host='localhost', port='5432', table_name='default_table'):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        
        with open(filepath, 'r') as file:
            for line in file:
                data_dict = json.loads(line)
                columns = ', '.join(data_dict.keys())
                placeholders = ', '.join(['%s'] * len(data_dict))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, list(data_dict.values()))
        
        conn.commit()
        print("Data inserted successfully!")
        
        cursor.close()
        conn.close()
    except (psycopg2.Error, IOError) as e:
        print(f"Error inserting data: {e}")

# Example usage:
if __name__ == "__main__":
    password = 'your_password'
    file_path = 'data.json'
    insert_dicts_from_file(password, file_path, table_name='your_table_name')
