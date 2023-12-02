from abc import ABC, abstractmethod

class DBManipulation(ABC):
    @abstractmethod
    def add_bank(self, connection, statement, bank_id, bank_name, address, email_address, mobile_no):
        pass

    @abstractmethod
    def delete_bank(self, connection, statement, bank_id):
        pass

    @abstractmethod
    def update_bank(self, connection, statement, bank_id, bank_name, address, email_address, mobile_no):
        pass

    @abstractmethod
    def add_employee(self, connection, statement, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        pass

    @abstractmethod
    def delete_employee(self, connection, statement, emp_id):
        pass

    @abstractmethod
    def update_employee(self, connection, statement, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        pass

    @abstractmethod
    def apply_loan(self, connection, statement, application_id, customer_id, loan_type, bank_id, interest, amount):
        pass

    @abstractmethod
    def update_loan(self, connection, statement, application_id, loan_status):
        pass

    @abstractmethod
    def register_customer(self, connection, statement, customer_id, customer_name, mobile_no, address, email_address, username, password):
        pass

    @abstractmethod
    def add_loan_types(self, connection, statement, bank_id, loan_type, interest_rate):
        pass

    @abstractmethod
    def update_loan_types(self, connection, statement, bank_id, loan_type, interest_rate):
        pass
