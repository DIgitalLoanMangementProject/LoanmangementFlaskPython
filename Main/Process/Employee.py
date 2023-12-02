from db.dbMainpulationImp import DBManipulationImpl
from db.dbretrivalImp import DBRetrieval
from .Customer import Customer

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

class Employee(Observable):
    def __init__(self,GlobalConnection):
        self.dml = DBManipulationImpl(GlobalConnection)
        self.drl = DBRetrieval(GlobalConnection)
        self.connection = GlobalConnection
        self.cursor = GlobalConnection.cursor()
        # Employee attributes
        self.emp_name = None
        self.emp_id = None
        self.emp_address = None
        self.email_address = None
        self.bank_id = None
        self.username = None
        self.password = None
        super().__init__()
    
    def set_name_id(self,name,id):
        self.emp_name=name
        self.emp_id=id

    def add_employee(self, cursor, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        self.dml.add_employee(cursor, emp_id, emp_name, emp_address, email_address, bank_id, username, password)

    def update_employee(self, cursor, emp_id, emp_name, emp_address, email_address, bank_id, username, password):
        self.dml.update_employee(cursor, emp_id, emp_name, emp_address, email_address, bank_id, username, password)

    def delete_employee(self, cursor, emp_id):
        self.dml.delete_employee(cursor, emp_id)

    def emp_login(self, cursor, username, password):
        return self.drl.validate_employee_login(cursor, username, password)

    def view_applications(self, cursor):
        return self.drl.get_all_loans(cursor)

    def update_loan_status(self, cursor, application_id, loan_status):
        self.dml.update_loan( application_id, loan_status)
        # Update observers if necessary
        self.update_change(application_id)

    # Implement observer pattern if necessary
    def update_change(self,application_id):
        # Your observer pattern implementation
        observer_customer_id = self.drl.get_customer_id_by_appln(self.cursor,application_id)
        self.add_observer(Customer.init_by_id(self.connection,observer_customer_id))
        self.notify_observers()

    def get_pending_loans(self, cursor):
        return self.drl.get_pending_loans(cursor)

# Example usage
# Assuming you have a database cursor set up (cursor)
# employee = Employee()
# employee.emp_login(cursor, username, password)
