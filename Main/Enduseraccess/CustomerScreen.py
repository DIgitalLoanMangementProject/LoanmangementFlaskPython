# Assuming Loan, Bank, Customer, and specific Loan types (AgricultureLoan, EducationLoan, etc.) are defined classes
from Process.AgricultureLoan import AgricultureLoan
from Process.Bank import Bank
from Process.Customer import Customer
from Process.EducationLoan import EducationLoan
from Process.GoldLoan import GoldLoan
from Process.HomeLoan import HomeLoan
from Process.Loan import Loan
from Process.PersonalLoan import PersonalLoan
from Process.VechileLoan import VechileLoan

class CustomerScreen:
    def __init__(self,connection, customer_id,customer_name):
        self.connection = connection
        self.loan = None
        self.bank = Bank(connection)
        self.customer = Customer(connection, customer_id,customer_name)

    def customer_inside_menu(self, username):
        print(f"Hello customer {username.split('-')[1]}")
        print("Please choose from the options given below:")
        print("1 - Apply for a Loan")
        print("2 - View Status of the applied Loan")
        print("3 - To logout of the application")

    def customer_tasks(self, username, cursor):
        while True:
            self.customer_inside_menu(username)
            choice = int(input("Please enter your choice: "))

            if choice == 1:
                self.apply_loan(username, cursor)
            elif choice == 2:
                self.status_loan( )
            elif choice == 3:
                break
            else:
                print("Please enter a valid option")

    # def apply_loan(self, username, cursor):
    #     customer_id = username.split("-")[0]
    #     bank_details = self.bank.get_loan_types(cursor)
    #     for detail in bank_details:
    #         print(detail)

    #     # Additional implementation as in Java code...
    #     # This will depend on how your Bank and Loan classes are implemented in Python

    def apply_loan(self,username, cursor):
        customer_id, username = username.split("-")
        j = 0
        bank_details = [None] * 10
        details = self.bank.get_loan_types(cursor)
        print(details)
        curr, prev = "", ""
        con = self.connection
        
        for i in range(len(details)):
            if details[i] is None:
                break

            curr = details[i].split("***")[0]
            temp = details[i].split("***", 2)[2]

            if not prev == curr:
                print("Bank Name :- " + temp)
                bank_details[j] = details[i].split("***")[:2]
                j += 1
                print("--- Offered Loans are ---\n      Type of the Loan --- Interest Rate")
                prev = curr
            print("   " , *temp.split("***"),sep ="   ")

        continue_process = "yes"
        
        while True:
            if continue_process == "no":
                break

            print("Bank ID **** Bank Name")
            
            for k in range(len(bank_details)):
                if bank_details[k] is None:
                    break
                print("***".join(bank_details[k]))

            print("Please enter the bank ID from which you want to apply for a loan:")
            bank_id = input()

            loan_data = self.bank.get_loan_type(cursor, bank_id)
            
            print("Type of the Loan --- Interest Rate")
            
            for k in range(len(loan_data)):
                if loan_data[k] is not None:
                    print(loan_data[k])

            print("Please enter the type of loan you need:")
            loan_needed = input().lower()

            print("Please enter the amount of loan you need:")
            amount = input()
            c= self.customer
            l = self.loan

            if loan_needed == "agriculture loan":
                l = AgricultureLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            elif loan_needed == "education loan":
                l = EducationLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            elif loan_needed == "home loan":
                l = HomeLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            elif loan_needed == "personal loan":
                l = PersonalLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            elif loan_needed == "vehicle loan":
                l = VechileLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            elif loan_needed == "gold loan":
                l = GoldLoan(con)
                c.apply_loan( cursor, l, customer_id, bank_id, amount)
            else:
                print("Please enter a valid loan type from the provided options above")
                continue_process = "yes"
                continue

            print("Do you wish to continue applying for another loan? Please enter 'yes' or 'no'")
            continue_process = input()


    def status_loan(self ):
        self.customer.update()

# Example usage
# Assuming you have set up database connection and obtained a cursor
# customer_screen = CustomerScreen()
# customer_screen.customer_tasks(username, cursor)
