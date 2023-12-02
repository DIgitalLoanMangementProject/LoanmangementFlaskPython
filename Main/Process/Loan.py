from abc import ABC, abstractmethod

class Loan(ABC):
    @abstractmethod
    def apply_loan(self, con, st, customer_id, bank_id, amount):
        pass