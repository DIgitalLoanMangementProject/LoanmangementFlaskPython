from db.dbconnection import DBConnection  # Assuming DBConnection is a defined class
from .loan_home import LoanHome  # Assuming LoanHome is a defined class
from .admin_home import AdminHome  # Assuming AdminHome is a defined class
from .customer_home import CustomerHome  # Assuming CustomerHome is a defined class
from .employee_home import EmployeeHome  # Assuming EmployeeHome is a defined class

Gloabalconnection = None
class LoanSystemHome:
    def __init__(self):
        self.db = DBConnection()
        GlobalConnection=self.db
        self.loan_home = LoanHome(GlobalConnection)
        self.admin_home = AdminHome(GlobalConnection)
        self.customer_home = CustomerHome(GlobalConnection)
        self.employee_home = EmployeeHome(GlobalConnection)
        self.connection = self.db
        self.statement = None

    def run(self):
        try:
            

            while True:
                self.loan_home.loan_menu()
                choice = int(input("Please enter the option: "))

                if choice == 1:
                    self.admin_home.admin_main(self.connection.cursor())
                elif choice == 2:
                    self.customer_home.customer_entry(self.connection.cursor())
                elif choice == 3:
                    self.employee_home.employee_entry(self.connection.cursor())
                elif choice == 4:
                    break
                else:
                    print("Invalid option, please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.statement:
                self.statement.close()
            if self.connection:
                self.connection.close()

if __name__ == "__main__":
    loan_system_home = LoanSystemHome()
    loan_system_home.run()
