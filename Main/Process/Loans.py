from abc import ABC, abstractmethod
from db.dbconnection import DBConnection  
from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval
class LoanApplier:

    def __init__(self):
        import random
        self.random_number = random.randint(1, 1000)
        print("getting db connection")
        # Initialization code here
        self.connection = DBConnection()
        print("type of dbconnection : ",type(self.connection))
        self.dml = DBManipulationImpl(self.connection)
        self.drl = DBRetrieval(self.connection)
        self.strategy: LoanDec = None
        self.cursor = self.connection.cursor()
        self._initialized = True
        print("self.random_number",self.random_number)
        self.loan_factory = LoanFactory()
    
    def apply_loan(self, customer_id, bank_id, amount):
        if self.strategy:
            self.strategy.apply_loan(self.cursor, customer_id, bank_id, amount)
        else:
            raise ValueError("Strategy not set")

    def set_strategy(self, strategy_type):
        self.strategy = self.loan_factory.create_loan(strategy_type, self.dml, self.drl)
        # return loanstrategy

""" def __init__(self,connection):
        self.dml = DBManipulationImpl(connection)
        self.drl = DBRetrieval(connection) """
# from db.dbMainpulationImp import DBManipulationImpl
# from db.dbretrivalImp import DBRetrieval
class LoanDec(ABC):
    @abstractmethod
    def apply_loan(self, cursor,customer_id, bank_id, amount):
        pass


class LoanFactory:
    @staticmethod
    def create_loan(strategy_type, dml, drl):
        if strategy_type == "Agriculture Loan":
            return AgricultureLoan(dml, drl)
        elif strategy_type == "Education Loan":
            return EducationLoan(dml, drl)
        elif strategy_type == "Gold Loan":
            return GoldLoan(dml, drl)
        elif strategy_type == "Home Loan":
            return HomeLoan(dml, drl)
        elif strategy_type == "Personal Loan":
            return PersonalLoan(dml, drl)
        elif strategy_type == "Vehicle Loan":
            return VehicleLoan(dml, drl)
        else:
            raise ValueError("Invalid strategy type")


class AgricultureLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, cursor, customer_id, bank_id, amount):
        loan_type = "agriculture loan"
        interest_rate = "3"
        application_id = self.drl.generate_loan_id(cursor)
        self.dml.apply_loan( application_id, customer_id, loan_type, bank_id, interest_rate, amount)


class EducationLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, cursor, customer_id, bank_id, amount):
        loan_type = "education loan"
        interest_rate = "9"
        application_id = self.drl.generate_loan_id(cursor)
        self.dml.apply_loan(application_id, customer_id, loan_type, bank_id, interest_rate, amount)


class GoldLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, cursor, customer_id, bank_id, amount):
        loan_type = "gold loan"
        interest_rate = "5"
        application_id = self.drl.generate_loan_id(cursor)
        self.dml.apply_loan(application_id, customer_id, loan_type, bank_id, interest_rate, amount)

class HomeLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, cursor, customer_id, bank_id, amount):
        loan_type = "Home loan"
        interest_rate = "7"
        application_id = self.drl.generate_loan_id(cursor)
        self.dml.apply_loan(application_id, customer_id, loan_type, bank_id, interest_rate, amount)

class PersonalLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, con, st, customer_id, bank_id, amount):
        loan_type = "personal loan"
        application_id = self.drl.generate_loan_id(st)
        interest_rate = "11.5"
        self.dml.apply_loan( application_id, customer_id, loan_type, bank_id, interest_rate, amount)

class VehicleLoan(LoanDec):
    def __init__(self,dml,drl):
        self.dml = dml
        self.drl = drl

    def apply_loan(self, st, customer_id, bank_id, amount):
        loan_type = "Vehicle Loan"
        application_id = self.drl.generate_loan_id(st)
        interest_rate = "12.5"
        self.dml.apply_loan( application_id, customer_id, loan_type, bank_id, interest_rate, amount)

        # Example us