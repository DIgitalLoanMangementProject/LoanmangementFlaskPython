from db.dbManipulation import DBManipulation
import mysql.connector
from abc import ABC, abstractmethod
class DBManipulationImpl(DBManipulation):
    def __init__(self,Gloabalconnection):
        self.connection = Gloabalconnection
        self.cursor = self.connection.cursor()

    def add_bank(self, bank_id, bank_name, address, email_address, mobile_no):
        try:
            query = "INSERT INTO bank(bankID, bankName, address, mobileno, email_adress) VALUES (%s, %s, %s, %s, %s)"
            values = (bank_id, bank_name, address, mobile_no, email_address)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in add_bank: {e}")

    def delete_bank(self, bank_id):
        try:
            query = "DELETE FROM bank WHERE bankID = %s"
            self.cursor.execute(query, (bank_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error in delete_bank: {e}")

    def update_bank(self, bank_id, bank_name, address, email_address, mobile_no):
        try:
            query = f"UPDATE bank SET bankName = '{bank_name}', address = '{address}', email_adress = '{email_address}', mobileno = '{mobile_no}' WHERE bankID = '{bank_id}'"
            # print(query)
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error in update_bank: {e}")

        try:
            self.cursor.execute("SELECT bankName FROM bank")
            print( [row[0] for row in self.cursor.fetchall()])
        except mysql.connector.Error as e:
            print(f"Error in get_bank_name: {e}")

    def add_employee(self, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        try:
            query = "INSERT INTO employee(empID, empName, empAddress, emailaddress, bankID, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (emp_id, emp_name, emp_address, email_address, bank_id, username, password)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in add_employee: {e}")

    def delete_employee(self, emp_id):
        try:
            query = "DELETE FROM employee WHERE empID = %s"
            self.cursor.execute(query, (emp_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error in delete_employee: {e}")

    def update_employee(self, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        try:
            query = "UPDATE employee SET empName = %s, empAddress = %s, emailaddress = %s, bankID = %s, username = %s, password = %s WHERE empID = %s"
            values = (emp_name, emp_address, email_address, bank_id, username, password, emp_id)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in update_employee: {e}")

    def update_loan_types(self, bank_id, loan_type, interest_rate):
        try:
            query = "UPDATE loantypes SET interestRate = %s WHERE bankID = %s AND loanType = %s"
            values = (interest_rate, bank_id, loan_type)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in update_loan_types: {e}")

    def add_loan_types(self, bank_id, loan_type, interest_rate):
        try:
            query = "INSERT INTO loantypes(bankID, loanType, interestRate) VALUES (%s, %s, %s)"
            values = (bank_id, loan_type, interest_rate)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in add_loan_types: {e}")

    def register_customer(self, customer_id, customer_name, mobile_no, address, email_address, username, password):
        try:
            query = "INSERT INTO customer(customerID, customerName, mobileno, address, emailaddress, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (customer_id, customer_name, mobile_no, address, email_address, username, password)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in register_customer: {e}")

    def apply_loan(self, application_id, customer_id, loan_type, bank_id, interest, amount):
        try:
            query = "INSERT INTO loan_details(applicationID, customerID, loanType, bankID, interest, loanStatus, amount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (application_id, customer_id, loan_type, bank_id, interest, "applied", amount)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in apply_loan: {e}")

    def update_loan(self, application_id, loan_status):
        try:
            query = "UPDATE loan_details SET loanStatus = %s WHERE applicationID = %s"
            values = (loan_status, application_id)
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(f"Error in update_loan: {e}")

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")