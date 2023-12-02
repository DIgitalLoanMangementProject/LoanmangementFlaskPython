import mysql.connector

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

        cursor = connection.cursor()

        # Check if the 'all_user_table' exists
        cursor.execute("SHOW TABLES LIKE 'all_user_table'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # Create the 'all_user_table' if it doesn't exist
            create_table_query = """
            CREATE TABLE all_user_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                user_type VARCHAR(50) NOT NULL,
                user_id_online VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(create_table_query)
            print("All User table created successfully")

        # Consolidate records from Customer table
        cursor.execute("SELECT customerID, customerName, password, 'customer' AS user_type FROM customer")
        customer_records = cursor.fetchall()
        print("Consolidating records from Customer table...")
        for record in customer_records:
            insert_query = "INSERT INTO all_user_table (user_id_online, user_type, name, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (record[0], record[3], record[1], record[2]))
        print("Records from Customer table inserted into 'all_user_table'")

        # Consolidate records from Employee table
        cursor.execute("SELECT empID, empName, password, 'employee' AS user_type FROM employee")
        employee_records = cursor.fetchall()
        print("Consolidating records from Employee table...")
        for record in employee_records:
            insert_query = "INSERT INTO all_user_table (user_id_online, user_type, name, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (record[0], record[3], record[1], record[2]))
        print("Records from Employee table inserted into 'all_user_table'")

        # Consolidate records from Admin table
        cursor.execute("SELECT adminID, username, password, 'admin' AS user_type FROM admin")
        admin_records = cursor.fetchall()
        print("Consolidating records from Admin table...")
        for record in admin_records:
            insert_query = "INSERT INTO all_user_table (user_id_online, user_type, name, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (record[0], record[3], record[1], record[2]))
        print("Records from Admin table inserted into 'all_user_table'")

        # Commit the changes to the database
        connection.commit()
        print("Records inserted into 'all_user_table' successfully")

except mysql.connector.Error as e:
    print("Error:", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
