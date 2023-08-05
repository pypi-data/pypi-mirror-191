import calculator_gskv_m1_s1 as calc
import random
def test_sum():
    """Tests summation"""
    for i in range(5):
        calculator=calc.Calculator()
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator.add(a)
        calculator.add(b)
        assert calculator.current_value==a+b, 'Summation error'

def test_subtraction():
    """Tests subtraction"""
    for i in range(5):
        calculator=calc.Calculator()
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator.subtract(a)
        calculator.subtract(b)
        assert calculator.current_value==0-a-b, 'Subtraction error'
    
def test_multiplication():
    """Tests multiplication"""
    for i in range(5):
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator=calc.Calculator(a)
        calculator.multiply(b)
        assert calculator.current_value==a*b, 'Multiplication error'

def test_division():
    """Tests multiplication"""
    for i in range(5):
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator=calc.Calculator(a)
        calculator.multiply(b)
        assert calculator.current_value==a*b, 'Multiplication error'

def test_exponentiation():
    """Tests exponentiation"""
    for i in range(5):
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator=calc.Calculator(a)
        calculator.exponentiate(b)
        assert calculator.current_value==a**b, 'Exponentiation error'

def test_root():
    """Tests root operation"""
    for i in range(5):
        a=random.uniform(1.01,50.01)
        b=random.uniform(1.02,50.02)
        calculator=calc.Calculator(a)
        calculator.root(b)
        assert calculator.current_value==a**(1/b), 'Root error'       

def test_reset():
    """Tests reset operation"""
    for i in range(5):
        a=random.uniform(1.01,50.01)
        calculator=calc.Calculator(a)
        calculator.reset()
        assert calculator.current_value==0, 'Calculator did not reset'       