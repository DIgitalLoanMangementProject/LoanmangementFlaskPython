class LoanHome:
    def __init__(self,GlobalConnection):
        self.connection = GlobalConnection
    def loan_menu(self):
        print("---------Welcome to the Loan Request System-------")
        print("Enter the below option to get into the needed system:")
        print("1 - Admin Login")
        print("2 - Customer Login")
        print("3 - Employee Login")
        print("4 - Exit")

# Example usage
# loan_home = LoanHome()
# loan_home.loan_menu()
