from abc import ABC, abstractmethod
import sqlite3

class LoanDec(ABC):
    @abstractmethod
    def apply_loan(self, con, st, customer_id, bank_id, amount):
        pass

# Example usage:
# class MyLoan(LoanDec):
#     def apply_loan(self, con, st, customer_id, bank_id, amount):
#         # Implement the logic for applying a loan
#         pass
