from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval
from .LoanDec import LoanDec
class PersonalLoan(LoanDec):
    def __init__(self,connection):
        self.dml = DBManipulationImpl(connection)
        self.drl = DBRetrieval(connection)

    def apply_loan(self, con, st, customer_id, bank_id, amount):
        loan_type = "personal loan"
        application_id = self.drl.generate_loan_id(st)
        interest_rate = "11.5"
        self.dml.apply_loan(con, st, application_id, customer_id, loan_type, bank_id, interest_rate, amount)
