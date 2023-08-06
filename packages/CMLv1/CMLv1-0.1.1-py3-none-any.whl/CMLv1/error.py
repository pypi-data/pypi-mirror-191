class BaseCheckoutError(RuntimeError):
    "Do not raise, but can be catched."
    pass

class IllegalInputError(BaseCheckoutError):
    "General illegal input."
    pass

class IllegalOperationError(BaseCheckoutError):
    "General illegal operation."
    pass

class OutOfRangeError(IllegalInputError):
    "Only for illegal inputs that ar out of range."
    pass

class DisabledValueError(IllegalInputError):
    "For illegal inputs that are currently disabled."
    pass

class LockedBalance(IllegalOperationError):
    "Operations on balances that are locked."
    pass