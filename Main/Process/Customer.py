

from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class Customer(Observer):

    @staticmethod
    def init_by_id(connection,id):
        drl = DBRetrieval(connection)
        username = drl.get_username_by_id(id)
        return Customer(connection,id,username)


    def __init__(self, connection,customer_id=None, username=None):
        self.dml = DBManipulationImpl(connection)
        self.drl = DBRetrieval(connection)
        self.customer_id = customer_id
        self.cursor = connection.cursor()
        self.username = username
        self.loan = None  # assuming Loan is a class
        self.notification = 0

    def register_customer(self, cursor, customer_id, customer_name, mobile_no, address, email_address, username, password):
        print("entered here")
        self.dml.register_customer(customer_id, customer_name, mobile_no, address, email_address, username, password)

    def validate_login(self, cursor, username, password):
        return self.drl.validate_customer_login(cursor, username, password)

    def apply_loan(self, cursor, loan, customer_id, bank_id, amount):
        self.loan = loan
        loan.apply_loan(cursor, customer_id, bank_id, amount)

    def view_loan_status(self, cursor, customer_id, username):
        print(f"Hello Customer {username}[{customer_id}], please see below the status of your loans")
        details = self.drl.get_loan_status(cursor, customer_id)
        # print(details)

        print("Application ID --- status of the loan application --- loan type --- Bank ID --- interest of the Loan --- amount")
        for detail in details:
            if detail is None:
                break
            print(detail)

    # Python doesn't use Observer pattern in the same way, this method needs to be adapted
    # depending on how you want to handle the update functionality in Python.
    def update(self, emp=None):
        if emp:
            self.addnotification(emp)
        else:
            self.view_loan_status(self.cursor,self.customer_id,self.username)
        
    
    def addnotification(self,emp=None):
        self.notification+=1
        print(f"{self.customer_id}-{self.username} received notification from {emp.emp_id}-{emp.emp_name}")


# Example usage
# Assuming you have set up database connection and obtained a cursor
# customer = Customer(customer_id="123", cursor=cursor, username="user123")
# customer.view_loan_status(cursor, "123", "user123")
