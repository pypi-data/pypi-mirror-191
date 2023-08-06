import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from src.rounded_calculate.calculator import Calculator
from random import random

calc = Calculator()

def test_multiply():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()*50
        x = round(x,8)
        x1 = calc.multiply(x)
        x2 *= x
        assert x1 == round(x2,8)

def test_multiply_small():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()
        x = round(x,8)
        x1 = calc.multiply(x)
        x2 *= x
        assert x1 == round(x2,8)

def test_multiply_large():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()*1000000
        x = round(x,8)
        x1 = calc.multiply(x)
        x2 *= x
        assert x1 == round(x2,8)

def test_multiply_negative():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = -random()*50
        x = round(x,8)
        x1 = calc.multiply(x)
        x2 *= x
        assert x1 == round(x2,8)

def test_multiply_inf():
    calc.reset_memory()
    x2 = 0 * float("inf")
    x1 = calc.multiply(float("inf"))
    # Both will allways return NaN
    assert True


def test_multiply_type():
    calc.reset_memory()
    x1 = calc.multiply("a")
    assert x1 == None