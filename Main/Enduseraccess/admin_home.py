# Assuming Bank, Employee, and DBRetrieval are defined classes


from Process.Bank import Bank
from Process.Employee import Employee
from db.dbretrivalImp import DBRetrieval


class AdminHome:
    def __init__(self,connection=None):
        self.bank = Bank(connection)
        self.employee = Employee(connection)
        self.connection = connection

    def admin_menu(self):
        print("Please choose the necessary operation:")
        print("1 - Add a new bank")
        print("2 - Update the Bank details")
        print("3 - Delete a new Bank")
        print("4 - Add an Employee")
        print("5 - Update an Employee")
        print("6 - Delete an Employee")
        print("7 - Exit")

    def admin_main(self, cursor):
        print("Hello Admin, Welcome back !!!")

        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        drl = DBRetrieval(self.connection)  # Assuming DBRetrieval has the necessary methods
        id = drl.validate_admin_login(cursor, username, password)
        print(id)

        if id:
            while True:
                self.admin_menu()
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    self.add_bank(cursor)
                elif choice == 2:
                    self.update_bank(cursor)
                elif choice == 3:
                    self.delete_bank(cursor)
                elif choice == 4:
                    self.add_employee(cursor)
                elif choice == 5:
                    self.update_employee(cursor)
                elif choice == 6:
                    self.delete_employee(cursor)
                elif choice == 7:
                    break
                else:
                    print("Please enter a valid option...")
        else:
            print("Invalid Credentials, Try Again...")

    def add_bank(self, cursor):
        bank_id = input("Enter your bank ID: ")
        bank_name = input("Enter your bank name: ")
        address = input("Enter your bank address: ")
        email_address = input("Enter your bank email address: ")
        mobile_no = input("Enter your bank mobile number: ")

        self.bank.add_bank(cursor, bank_id, bank_name, address, email_address, mobile_no)

    # Define other methods (update_bank, delete_bank, add_employee, etc.) similarly
    
    def update_bank(self, cursor):
        print("Existing Banks:")
        existing_banks = self.bank.get_bank_details(cursor)
        print("s.no | id | name|adress| email | monile no")
        for index, bank_details in enumerate(existing_banks, start=1):
            print(f"{index}. ",*bank_details,sep=" | ")

        try:
            choice = int(input("Enter the number of the bank you want to update: ")) - 1
            if 0 <= choice < len(existing_banks):
                bank_id = existing_banks[choice][0]
                new_bank_name = input("Enter the new bank name: ")
                new_address = input("Enter the new bank address: ")
                new_email_address = input("Enter the new bank email address: ")
                new_mobile_no = input("Enter the new bank mobile number: ")

                self.bank.update_bank(cursor, bank_id, new_bank_name, new_address, new_email_address, new_mobile_no)
                print("Bank updated successfully!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

