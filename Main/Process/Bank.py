# Assuming DBManipulation and DBRetrieval are defined classes in Python


from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval


class Bank:
    def __init__(self,connection):
        self.dml = DBManipulationImpl(connection)
        self.drl = DBRetrieval(connection)
        self.loan = None  # Assuming Loan is a defined class

    def get_loan_types(self, cursor):
        return self.drl.get_loan_types(cursor)

    def get_loan_type(self, cursor, bank_id):
        return self.drl.get_loan_type(cursor, bank_id)

    def add_bank(self, cursor, bank_id, bank_name, address, email_address, mobile_no):
        print(mobile_no)
        self.dml.add_bank(bank_id, bank_name, address, email_address, mobile_no)

    def delete_bank(self, cursor, bank_id):
        self.dml.delete_bank(bank_id)

    def update_bank(self, cursor, bank_id, bank_name, address, email_address, mobile_no):
        self.dml.update_bank(bank_id, bank_name, address, email_address, mobile_no)

    def get_bank_names(self, cursor):
        return self.drl.get_bank_name(cursor)
    
    def get_bank_details(self, cursor):
        return self.drl.get_bank_details(cursor)

    def get_bank_email_address(self, cursor, bank_id):
        return self.drl.get_bank_email(cursor, bank_id)

# Example usage
# Assuming you have a database cursor set up (cursor)
# bank = Bank()
# bank_names = bank.get_bank_names(cursor)
# print(bank_names)
