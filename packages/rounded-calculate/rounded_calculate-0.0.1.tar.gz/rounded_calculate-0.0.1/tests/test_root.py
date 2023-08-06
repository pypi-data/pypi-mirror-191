import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from src.rounded_calculate.calculator import Calculator
from random import random, randint
import math

calc = Calculator()

def test_root():
    calc.reset_memory()
    x2 = 10
    calc.add(10)
    for i in range(3):
        x = randint(1,10)
        x = round(x,8)
        x1 = calc.root(x)
        x2 = round(x2 **(1 / x),8)
        assert x1 == x2

def test_root_small():
    calc.reset_memory()
    x2 = 10
    calc.add(10)
    for i in range(3):
        x = random()
        x = round(x,8)
        x1 = calc.root(x)
        x2 = round(x2 **(1 / x),8)
        assert x1 == x2

def test_root_large():
    calc.reset_memory()
    x2 = 10
    calc.add(10)
    for i in range(3):
        try:
            x = math.floor(random()*100)
            x = round(x,8)
            x1 = calc.root(x)
            x2 = round(x2 **(1 / x),8)
            assert x1 == x2
        except ZeroDivisionError:
            continue

def test_root_negative():
    calc.reset_memory()
    x2 = 10
    calc.add(10)
    for i in range(2):
        x = -random()
        x = round(x,8)
        x1 = calc.root(x)
        x2 = round(x2 **(1 / x),8)
        assert x1 == x2

def test_root_inf():
    calc.reset_memory()
    x2 = 10 ** (1/ float("inf"))
    calc.add(10)
    x1 = calc.root(float("inf"))
    print(x1)
    assert x1 == x2

def test_root_zero():
    calc.reset_memory()
    x1 = calc.root(0)
    assert x1 == None


def test_root_type():
    calc.reset_memory()
    x1 = calc.root("a")
    assert x1 == None