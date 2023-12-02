from abc import ABC, abstractmethod

class DBRetrievalInterface(ABC):

    @abstractmethod
    def get_bank_name(self, cursor):
        pass

    @abstractmethod
    def get_bank_email(self, cursor, bank_id):
        pass

    @abstractmethod
    def get_loan_status(self, cursor, customer_id):
        pass

    @abstractmethod
    def get_customer_id(self, cursor, username):
        pass

    @abstractmethod
    def validate_customer_login(self, cursor, username, password):
        pass

    @abstractmethod
    def validate_employee_login(self, cursor, username, password):
        pass

    @abstractmethod
    def validate_admin_login(self, cursor, username, password):
        pass

    @abstractmethod
    def get_bank_id(self, cursor):
        pass

    @abstractmethod
    def get_loan_types(self, cursor):
        pass

    @abstractmethod
    def get_loan_type(self, cursor, bank_id):
        pass

    @abstractmethod
    def generate_loan_id(self, cursor):
        pass

    @abstractmethod
    def get_all_loans(self, cursor):
        pass

    @abstractmethod
    def get_pending_loans(self, cursor):
        pass
