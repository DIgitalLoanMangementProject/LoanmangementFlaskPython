import mysql.connector

# Define admin credentials
admin_username = "a"
admin_password = "a"

# Create a MySQL database connection
try:
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="adminPass",
        database="loan_management_system"
    )

    if connection.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES LIKE 'admin'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # Create the admin table if it doesn't exist
            create_table_query = """
            CREATE TABLE admin (
                adminID INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(create_table_query)
            print("Admin table created successfully")

        # Check if the admin already exists (optional)
        cursor.execute("SELECT adminID FROM admin WHERE username = %s", (admin_username,))
        admin_exists = cursor.fetchone()

        if admin_exists:
            print("Admin already exists")
        else:
            # Insert admin credentials into the admin table
            insert_query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
            admin_data = (admin_username, admin_password)
            cursor.execute(insert_query, admin_data)

            # Commit the changes to the database
            connection.commit()

            print("Admin credentials inserted successfully")

except mysql.connector.Error as e:
    print("Error:", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
