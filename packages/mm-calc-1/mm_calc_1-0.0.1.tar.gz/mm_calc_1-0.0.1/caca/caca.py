class Calculator:

    def __init__(self, add, substract, divide, multiply, nr, memory=0):
        self.add = add
        self.substract = substract
        self.divide = divide
        self.multiply = multiply
        self.memory = memory
        self.nr = nr

    def add(x,y):
        return(x+y)

    def substract(x,y):
        return(x-y)

    def multiply(x,y):
        return(x*y)

    def divide(x,y):
        return(x/y)

    def nr(y,x):
        return(abs(x)**(1/y))

