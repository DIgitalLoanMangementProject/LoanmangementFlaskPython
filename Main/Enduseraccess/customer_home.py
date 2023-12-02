# Assuming Customer and CustomerScreen are defined classes


from Enduseraccess.CustomerScreen import CustomerScreen
from Process.Customer import Customer


class CustomerScreen:
    def __init__(self,connection):
        self.connection= connection
        self.customer = Customer(connection)

    def customer_menu(self):
        print("******* Hello Dear Customer, we have been waiting for you *******")
        print("Please choose from the below options:")
        print("1 - Already with us? Please choose '1' to sign in")
        print("2 - Willing to join us? Please choose '2' to sign up")
        print("3 - Entered accidentally? Enter '3' to leave but we are expecting you soon...")

    def login(self, cursor):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        return self.customer.validate_login(cursor, username, password)

    def customer_register(self, cursor):
        customer_id = input("Please enter the customer ID: ")
        customer_name = input("Please enter the customer name: ")
        address = input("Please enter the customer address: ")
        email_address = input("Please enter the customer email address: ")
        mobile_no = input("Please enter the mobile number: ")
        username = input("Please enter the username of customer: ")
        password = input("Please enter the password: ")

        self.customer.register_customer(cursor, customer_id, customer_name, mobile_no, address, email_address, username, password)

    def customer_entry(self, cursor):
        while True:
            self.customer_menu()
            choice = int(input("Please enter your choice: "))

            if choice == 1:
                customer_id,customer_name = self.login(cursor)
                if customer_id:
                    customer_screen = CustomerScreen(self.connection, customer_id,customer_name)
                    customer_screen.customer_tasks(f"{customer_id}-{customer_name}", cursor)
                else:
                    print("Please check your username, password and try again")
            elif choice == 2:
                self.customer_register(cursor)
            elif choice == 3:
                break
            else:
                print("Please choose a valid choice")

# Example usage
# Assuming you have set up database connection and obtained a cursor
# customer_home = CustomerHome()
# customer_home.customer_entry(cursor)
