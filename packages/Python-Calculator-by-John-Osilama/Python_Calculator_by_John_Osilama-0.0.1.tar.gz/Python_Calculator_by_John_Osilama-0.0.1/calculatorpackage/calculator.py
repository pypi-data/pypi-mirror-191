# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 06:00:18 2023

@author: John
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 23:32:23 2023

@author: John
"""
import math

""" Calculator class """
class Calculator:
    
    """ default constructor of the Calculator class, 
    it is called everytime an object is created """
    def __init__(self):
        pass
    
        """ The add method takes in two parameters,
        x and y, it returns the addition of x and y """
    def add(self, x, y):
        return x + y
    
    """ The subtract method takes in two parameters,
    x and y, it returns the subtraction of x and y """
    def subtract(self, x, y):
        return x - y
    
    """ The multiply method takes in two parameters,
    x and y, it returns the multiplication of x and y """
    def multiply(self, x, y):
        return x * y
    
    """ The divide method takes in two parameters,
    x and y, it returns the division of x and y """
    def divide(self, x, y):
        return x / y
    
    """ The square root method takes in two parameters,
    x and y, it returns the addition of x and y """
    def squareRoot(self, x):
        return math.sqrt(x)
    
    """ Solve function of the calculator class """
    def solve(self):
            while True:
                
                """ take input from the user """
                choice = input("Enter choice(1/2/3/4/5): ")

                """ check if choice is one of the four options """
                if choice in ('1', '2', '3', '4'):
                    try:
                        num1 = float(input("Enter first number: "))
                        num2 = float(input("Enter second number: "))
                        
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue

                    if choice == '1':
                        print(num1, "+", num2, "=", self.add(num1, num2))

                    elif choice == '2':
                        print(num1, "-", num2, "=", self.subtract(num1, num2))

                    elif choice == '3':
                        print(num1, "*", num2, "=", self.multiply(num1, num2))

                    elif choice == '4':
                        print(num1, "/", num2, "=", self.divide(num1, num2))
                        
                    elif choice == '5':
                        print("sqrt", "of", num1, "=", self.squareRoot(num1))
            
                    """ check if user wants another calculation, and break while loop,
                    if answer is no """
                    next_calculation = input("Let's do next calculation? (yes/no): ")
                    if next_calculation == "no":
                       break
                if choice == '5':
                    num1 = float(input("Enter a number: "))
                    print("sqrt", "of", num1, "=", self.squareRoot(num1))

                    """ check if user wants another calculation, and break while loop,
                    if answer is no """
                    next_calculation = input("Let's do next calculation? (yes/no): ")
                    if next_calculation == "no":
                       break
                else:
                    print("Invalid Input")


    

                
print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")
print("5.Square Root")

""" creating object of the class """
calculator = Calculator()

""" calling the instance method using the object calculator """
calculator.solve()
