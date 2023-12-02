# Assuming Employee class is defined in Python
from Process.Employee import Employee


class EmployeeHome:
    def __init__(self,connection):
        self.employee = Employee(connection)

    def employee_menu(self):
        print("Please select the appropriate option:")
        print("1 - Display all the Loan applications")
        print("2 - Update the status of the application")
        print("3 - Log out of the System")

    def employee_entry(self, cursor):
        print("Hello Dear Employee, Welcome back !!!")

        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        auth = self.employee.emp_login(cursor, username, password)
        if auth:
            self.employee.set_name_id(auth[0],auth[1])
            while True:
                self.employee_menu()
                choice = int(input("Please enter your choice: "))

                if choice == 1:
                    self.display_all_loans(cursor)
                elif choice == 2:
                    self.update_pending_loans(cursor)
                elif choice == 3:
                    break
                else:
                    print("Please choose a valid choice")
        else:
            print("Please check your credentials...")

    def display_all_loans(self, cursor):
        data = self.employee.view_applications(cursor)
        print("Application ID --- Customer ID --- Type of the Loan --- ID of the Bank --- Interest Rate of the Loan --- Status of the Loan --- Amount")
        print("--------------------------------------------------------------------------------------------------------------------------------------")

        for entry in data:
            print(entry)

    def update_pending_loans(self, cursor):
        data = self.employee.get_pending_loans(cursor)
        print("Application ID --- Customer ID --- Type of the Loan --- ID of the Bank --- Interest Rate of the Loan --- Status of the Loan --- Amount")
        print("--------------------------------------------------------------------------------------------------------------------------------------")

        for entry in data:
            print(entry)

        application_id = int(input("Please enter the application ID of the loan for which status has to be updated: "))
        loan_status = input("Please enter the status you want to update (all in small letters): ")
        self.employee.update_loan_status(cursor, application_id, loan_status)
        print(f"The status of the loan with application ID {application_id} has been updated")

# Example usage
# Assuming you have set up a database connection and obtained a cursor
# employee_home = EmployeeHome()
# employee_home.employee_entry(cursor)
