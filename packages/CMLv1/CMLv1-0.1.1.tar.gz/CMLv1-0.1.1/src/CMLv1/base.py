import error

__version__ = (0, 1, 0)
class Base:
    pass

class Balance(Base):
    def __init__(self, balance, locked=False):
        self.__balance = balance
        self.__locked = locked

    def getbalance(self):
        return self.__balance

    def setbalance(self, balance):
        if self.__locked:
            raise error.LockedBalance("Balance is already locked.")
        if not (isinstance(balance, int) or isinstance(balance,float)) or balance < 0 or balance > 10 ** 7 :
            raise error.OutOfRangeError("Given value out of range.")
        self.__balance = balance
        return

    def setlocked(self):
        self.__locked = True

    def __add__(self, b):
        if not isinstance(b, Balance):
            raise TypeError("Operation require 2 or more balances.")
        self.__balance = self.__balance + b.getbalance()
        return self

    def __sub__(self, b):
        if not isinstance(b, Balance):
            raise TypeError("Operation require 2 or more balances.")
        self.__balance = self.__balance - b.getbalance()
        return self

    def __mul__(self, b):
        if not isinstance(b, float):
            raise TypeError("Operation require a balance and an float, not 2 balances.")
        self.__balance = self.__balance + b
        return self

    def __div__(self, b):
        if not isinstance(b, float):
            raise TypeError("Operation require a balance and an float, not 2 balances.")
        self.__balance = self.__balance + b
        return self

class BaseProduct_numprice(Base):
    def __init__(self, name, price):
        self.name = name
        self.__price = price
        return
    def getprice(self):
        return self.__price
    def setprice(self, price):
        self.__price = price
        return 0
    def fmt_print(self):
        print(f"Product: {self.name} ${self.getprice()}")
        return 0
    def fmt(self):
        return f"Product: {self.name} ${self.__price}"

class BaseProduct_balprice(Base):
    def __init__(self, name, price_as_balance):
        self.name = name
        self.price = Balance(price_as_balance)
        return
    def getprice(self):
        return self.price.getbalance()
    def get_raw(self):
        return self.price
    def setprice(self, price):
        self.price.setbalance(price)
        return
    def fmt_print(self):
        print(f"Product: {self.name} ${self.price.getbalance()}")
        return
    def fmt(self):
        return f"Product: {self.name} ${self.price.getbalance()}"

