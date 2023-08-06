import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from src.rounded_calculate.calculator import Calculator
from random import random

calc = Calculator()

def test_divide():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()*50
        x = round(x,8)
        x1 = calc.divide(x)
        x2 = round(x2 / x, 8)
        assert x1 == x2

def test_divide_small():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()
        x = round(x,8)
        x1 = calc.divide(x)
        x2 = round(x2 / x, 8)
        assert x1 == x2

def test_divide_large():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()/1000000
        x = round(x,8)
        x1 = calc.divide(x)
        x2 = round(x2 / x, 8)
        assert x1 == x2

def test_divide_negative():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = -random()/50
        x = round(x,8)
        x1 = calc.divide(x)
        x2 = round(x2 / x, 8)
        assert x1 == x2

def test_divide_inf():
    calc.reset_memory()
    x2 = 0 / float("inf")
    x1 = calc.divide(float("inf"))
    print(x1)
    assert x1 == x2

def test_divide_zero():
    calc.reset_memory()
    x1 = calc.divide(0)
    assert x1 == None


def test_divide_type():
    calc.reset_memory()
    x1 = calc.divide("a")
    assert x1 == None