import mysql.connector

# Function to add an employee
def add_employee(cursor, empID, empName, empAddress, emailaddress, bankID, username, password):
    query = "INSERT INTO employee (empID, empName, empAddress, emailaddress, bankID, username, password) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (empID, empName, empAddress, emailaddress, bankID, username, password))
    # cursor.connection.commit()
    print("Employee added successfully!")

# Database connection parameters
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "adminPass",
    "database": "loan_management_system"
}

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Prompt for employee information
    empID = input("Enter Employee ID: ")
    empName = input("Enter Employee Name: ")
    empAddress = input("Enter Employee Address: ")
    emailaddress = input("Enter Email Address: ")
    bankID = input("Enter Bank ID: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    # Add the employee to the database
    add_employee(cursor, empID, empName, empAddress, emailaddress, bankID, username, password)
    
    print("Employee added successfully!")
    connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
