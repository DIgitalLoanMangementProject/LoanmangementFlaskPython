
from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval
from .LoanDec import LoanDec

class AgricultureLoan(LoanDec):
    def __init__(self,connection):
        self.dml = DBManipulationImpl(connection)
        self.drl = DBRetrieval(connection)

    def apply_loan(self, cursor, customer_id, bank_id, amount):
        loan_type = "agriculture loan"
        interest_rate = "3"
        application_id = self.drl.generate_loan_id(cursor)
        self.dml.apply_loan( application_id, customer_id, loan_type, bank_id, interest_rate, amount)

# Example usage
# Assuming you have set up a database connection and obtained a cursor
# agriculture_loan = AgricultureLoan()
# agriculture_loan.apply_loan(cursor, customer_id, bank_id, amount)
