import mysql.connector

# Define your database connection details
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'adminPass',
    'database': 'loan_management_system'
}

# Establish a connection to the database
connection = mysql.connector.connect(**config)

if connection.is_connected():
    print("Connected to MySQL database")

    cursor = connection.cursor(dictionary=True)

    # Tables to fetch records from
    tables = ['bank', 'employee', 'customer', 'loan_details', 'loantypes', 'admin', 'all_user_table']

    # Fetch and print records from each table
    for table in tables:
        print(f"Records from {table}:")
        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()
        for record in records:
            print(record)
        print()

    # Close cursor and connection
    cursor.close()
    connection.close()
    print("MySQL connection closed")
else:
    print("Connection failed.")
