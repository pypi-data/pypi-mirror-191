# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 06:00:57 2023

@author: John
"""

from calculator import Calculator
import unittest

class CalculatorTestCase(unittest.TestCase):
    
    def test_add(self):
     calc = Calculator()
     self.assertEqual(10, calc.add(7, 3))
     
    def test_subtract(self):
      calc = Calculator()
      self.assertEqual(12, calc.subtract(15, 3)) 
      
    def test_multiply(self):
     calc = Calculator()
     self.assertEqual(30, calc.multiply(5, 6))
     
    def test_divide(self):
        calc = Calculator()
        self.assertEqual(5, calc.divide(10, 2))
        
    def test_squareRoot(self):
        calc = Calculator()
        self.assertEqual(7, calc.squareRoot(49))
     
    if __name__ == '__main__':
     unittest.main()