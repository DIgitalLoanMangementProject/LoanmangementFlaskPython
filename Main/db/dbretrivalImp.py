from .dbretrival import DBRetrievalInterface
import mysql.connector
from abc import ABC, abstractmethod

class DBRetrieval(DBRetrievalInterface):
    def __init__(self,GlobalConnection):
        self.connection = GlobalConnection
        self.cursor = self.connection.cursor()
        # print(type(self.cursor))
        # print(self.cursor is None)
        # exit()
    
    def get_bank_details(self, cursor):
        try:
            cursor.execute("SELECT *  FROM bank")
            return [row for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_bank_name: {e}")

    def get_bank_name(self, cursor):
        try:
            cursor.execute("SELECT bankName FROM bank")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_bank_name: {e}")

    def get_bank_email(self, cursor, bank_id):
        try:
            cursor.execute("SELECT email_adress FROM bank WHERE bankID = %s", (bank_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Error in get_bank_email: {e}")

    def get_loan_status(self, cursor, customer_id):
        try:
            cursor.execute("SELECT applicationID, loanStatus, loanType, bankID, interest, amount FROM loan_details WHERE customerID = %s", (customer_id,))
            return [" --- ".join(map(str, row)) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_loan_status: {e}")

    def get_customer_id(self, cursor, username):
        try:
            cursor.execute("SELECT customerID FROM customer WHERE username = %s", (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Error in get_customer_id: {e}")
    
    def validate_customer_login(self, cursor, username, password):
        try:
            cursor.execute("SELECT customerID, username FROM customer WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result if result else None
        except mysql.connector.Error as e:
            print(f"Error in validate_customer_login: {e}")
    
    def validate_admin_login(self, cursor, username, password):
        try:
            cursor.execute("SELECT adminID FROM admin WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Error in validate_admin_login: {e}")

    def get_bank_id(self, cursor):
        # Implementation will depend on the context. Placeholder implementation:
        try:
            cursor.execute("SELECT bankID FROM bank")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_bank_id: {e}")
    
    def get_loan_types(self, cursor):
        try:
            cursor.execute("SELECT DISTINCT b.bankID, bankName, loanType, interestRate FROM loantypes l JOIN bank b ON b.bankID = l.bankID")
            return ["***".join(map(str, row)) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_loan_types: {e}")

    def get_loan_type(self, cursor, bank_id):
        try:
            cursor.execute("SELECT DISTINCT loanType, interestRate FROM loantypes WHERE bankID = %s", (bank_id,))
            return [" --- ".join(map(str, row)) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_loan_type: {e}")

    def generate_loan_id(self, cursor):
        try:
            cursor.execute("SELECT MAX(applicationID) FROM loan_details")
            result = cursor.fetchone()
            return result[0] + 1 if result and result[0] else 1
        except mysql.connector.Error as e:
            print(f"Error in generate_loan_id: {e}")
    
    def get_all_loans(self, cursor):
        try:
            cursor.execute("SELECT * FROM loan_details")
            return [" --- ".join(map(str, row)) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_all_loans: {e}")

    def get_pending_loans(self, cursor):
        try:
            cursor.execute("SELECT * FROM loan_details WHERE loanStatus != 'success'")
            return [" --- ".join(map(str, row)) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error in get_pending_loans: {e}")
    
    def validate_employee_login(self, cursor, username, password):
        try:
            cursor.execute("SELECT empName,empID FROM employee WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            # print("==>",result)
            return result if result else None
        except mysql.connector.Error as e:
            print(f"Error in validate_employee_login: {e}")

    def get_customer_id_by_appln(self, cursor, applnid):
        try:
            cursor.execute("SELECT customerID FROM loan_details WHERE applicationID = %s", (applnid,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Error in get_customer_id: {e}")

    def get_username_by_id(self,id):
        try:
            self.cursor.execute("SELECT username FROM customer WHERE customerID = %s", (id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            print(f"Error in get_customer_id: {e}")