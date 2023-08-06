class Calculator:
    # Define Calculator class.
    # 
    #  All calculations made by class is rounded with 8 symbols precision.
    #  Calculator memory is controled by Memory class.
    #  
    #  This class has methods to do perform:
    #  I. Calculations: 
    #    Addition, substraction, multiplication,
    #    division, taking a (n) root of a number.
    #  II. Memory related methods:
    #    Reset memory, undo last operation stored
    #    in Memory class, print calculator history.
    def __init__(self):
        self.memory = Memory()

    def add(self, operand):
        # Calculate addition by the given operand.
        # 
        # Calculations are based on the last Memory.history.total value.
        try:
            base = self.memory.history[-1].total
            total = round(base + operand, 8)
            self.memory.memory_add_item(base, "+", operand, total)
            return total
        except:
            print(f"Provided operand '{operand}' is not valid in {self.add.__name__} method")

    def substract(self, operand):
        # Calculate substraction by the given operand.
        # 
        # Calculations are based on the last Memory.history.total value.
        try:
            base = self.memory.history[-1].total
            total = round(base - operand, 8)
            self.memory.memory_add_item(base, "-", operand, total)
            return total
        except:
            print(f"Provided operand '{operand}' is not valid in {self.substract.__name__} method")

    def multiply(self, operand):
        # Calculate multiplication by the given operand.
        # 
        # Calculations are based on the last Memory.history.total value.
        try:    
            base = self.memory.history[-1].total
            total = round(base * operand, 8)
            self.memory.memory_add_item(base, "*", operand, total)
            return total
        except:
            print(f"Provided operand '{operand}' is not valid in {self.multiply.__name__} method")

    def divide(self, operand):
        # Calculate division by the given operand.
        # 
        # Calculations are based on the last Memory.history.total value.
        try:
            base = self.memory.history[-1].total
            total = round(base / operand, 8)
            self.memory.memory_add_item(base, "/", operand, total)
            return total
        except:
            print(f"Provided operand '{operand}' is not valid in {self.divide.__name__} method")

    def root(self, power):
        # Calculate root of given power.
        # 
        # Calculations are based on the last Memory.history.total value.
        try:
            base = self.memory.history[-1].total
            total = round(base ** (1/power), 8)
            self.memory.memory_add_item(base, "** 1 /", power, total)
            return total
        except:
            print(f"Provided power of root '{power}' is not valid in {self.root.__name__} method")


    def reset_memory(self):
        # Delete calculator memory object and initialize new Memory object.
        del self.memory
        self.memory = Memory()

    def undo(self):
        # Remove last item in Memory.history list.
        # 
        # Calls Memory class method.
        self.memory.memory_remove_last()

    def print_history(self):
        # Print history of all operations stored in Memory.history.
        for item in self.memory.history:
            print(f"{item.base} {item.operation} {item.operand} = {+ item.total}")

class Memory:
    # Calculator module memory control.

    def __init__(self):
        self.history = []
        self.history.append(self.History_item(0, "Initial value", 0, 0))

    class History_item:
        # History item construct to store at Memory.history.

        def __init__(self, base, operation, operand, total):
            self.base = base
            self.operation = operation
            self.operand = operand
            self.total = total

    def memory_add_item(self, base, operation, operand, total):
        # Add new Memory.history entry using History_item construct.
        new_history_item = self.History_item(base, operation, operand, total)
        self.history.append(new_history_item)

    def memory_remove_last(self):
        # Remove last item of Memory.history.
        self.history.pop()