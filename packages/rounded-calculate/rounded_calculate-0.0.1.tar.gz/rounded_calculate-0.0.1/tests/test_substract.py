import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from src.rounded_calculate.calculator import Calculator
from random import random

calc = Calculator()

def test_substract():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()*50
        x = round(x,8)
        x1 = calc.substract(x)
        x2 = round(x2 - x,8)
        assert x1 == x2

def test_substract_small():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()
        x = round(x,8)
        x1 = calc.substract(x)
        x2 = round(x2 - x, 8)
        assert x1 == x2

def test_substract_large():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = random()*1000000
        x = round(x,8)
        x1 = calc.substract(x)
        x2 = round(x2 - x, 8)
        assert x1 == x2

def test_substract_negative():
    calc.reset_memory()
    x2 = 0
    for i in range(30):
        x = -random()*50
        x = round(x,8)
        x1 = calc.substract(x)
        x2 = round(x2 - x, 8)
        assert x1 == x2

def test_substract_inf():
    calc.reset_memory()
    x2 = 0 - float("inf")
    x1 = calc.substract(float("inf"))
    assert x1 == x2


def test_substract_type():
    calc.reset_memory()
    x1 = calc.substract("a")
    assert x1 == None
