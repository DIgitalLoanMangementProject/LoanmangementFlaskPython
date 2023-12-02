import mysql.connector

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("creating instance")
            cls._instance = super().__new__(cls)
            cls._instance.initialize(*args, **kwargs)
            cls._instance.connect_db()
            cls._instance.create_database("loan_management_system")
            # cls._instance.list_tables()
            # cls._instance.create_tables()
            # cls._instance.list_tables()
        return cls._instance

    def initialize(self, url="localhost", port=3306, username="root", password="adminPass", database=None):
        self.url = url
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

        # Initialize database operations
        

    def connect_db(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="adminPass",
                database=self.database
            )
            return self.connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            exit(1)

    def create_database(self, database_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
            self.connection.database = database_name
            print(f"Database '{database_name}' created successfully.")
            self.database = database_name
            print(f"self.database=> {self.database}")
            self.connection.close()
            self.connect_db()
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def create_tables(self):
        try:
            cursor = self.connection.cursor()

            # Create 'bank' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bank (
                    bankID VARCHAR(255) PRIMARY KEY,
                    bankName VARCHAR(255),
                    address VARCHAR(255),
                    mobileno VARCHAR(20),
                    email_adress VARCHAR(255)
                );
            ''')

            # Create 'employee' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employee (
                    empID VARCHAR(255) PRIMARY KEY,
                    empName VARCHAR(255),
                    empAddress VARCHAR(255),
                    emailaddress VARCHAR(255),
                    bankID VARCHAR(255),
                    username VARCHAR(255),
                    password VARCHAR(255),
                    FOREIGN KEY (bankID) REFERENCES bank(bankID)
                );
            ''')

            # Create 'customer' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customer (
                    customerID VARCHAR(255) PRIMARY KEY,
                    customerName VARCHAR(255),
                    mobileno VARCHAR(20),
                    address VARCHAR(255),
                    emailaddress VARCHAR(255),
                    username VARCHAR(255),
                    password VARCHAR(255)
                );
            ''')

            # Create 'loan_details' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loan_details (
                    applicationID INT PRIMARY KEY AUTO_INCREMENT,
                    customerID VARCHAR(255),
                    loanType VARCHAR(255),
                    bankID VARCHAR(255),
                    interest DECIMAL(5, 2),
                    loanStatus VARCHAR(50),
                    amount DECIMAL(10, 2),
                    FOREIGN KEY (customerID) REFERENCES customer(customerID),
                    FOREIGN KEY (bankID) REFERENCES bank(bankID)
                );
            ''')

            # Create 'loantypes' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loantypes (
                    loanTypeID INT PRIMARY KEY AUTO_INCREMENT,
                    bankID VARCHAR(255),
                    loanType VARCHAR(255),
                    interestRate DECIMAL(5, 2),
                    FOREIGN KEY (bankID) REFERENCES bank(bankID)
                );
            ''')

            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables {e}")
            exit(1)

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection is closed")
    
    def list_tables(self):
        if self.database is None:
            print("No database selected.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        except Exception as e :
            print(f"Error listing tables {e}")

def main():
    print("Initializing database manager...")
    db_manager = DatabaseManager(username="root", password="adminPass")

    print("Connecting to MySQL server...")
    db_manager.connect_db()

    print("Creating 'loan_management_system' database...")
    db_manager.create_database("loan_management_system")

    print("Listing tables")
    db_manager.list_tables()

    print("Creating tables in the database...")
    db_manager.create_tables()

    print("Listing tables")
    db_manager.list_tables()

    print("Closing database connection...")
    db_manager.close_connection()
    print("All operations completed successfully.")

if __name__ == '__main__':
    main()


# def DBConnection():
#     print("Initializing database manager...")
#     db_manager = DatabaseManager(username="root", password="adminPass")

#     print("Connecting to MySQL server...")
#     db_manager.connect_db()

#     print("Creating 'loan_management_system' database...")
#     db_manager.create_database("loan_management_system")

#     print("Listing tables")
#     db_manager.list_tables()

#     print("Creating tables in the database...")
#     db_manager.create_tables()

#     print("Listing tables")
#     db_manager.list_tables()

#     return db_manager.connection

def DBConnection():
    DatabaseManager()
    return DatabaseManager().connection