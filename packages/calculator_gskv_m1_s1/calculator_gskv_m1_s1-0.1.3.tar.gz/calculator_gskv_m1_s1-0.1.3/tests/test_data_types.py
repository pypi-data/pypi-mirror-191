import calculator_gskv_m1_s1 as calc
import pytest

def test_starting_value_type():
    """Tests whether non int or float values can be passed as starting value"""
    with pytest.raises(AssertionError):
        calculator=calc.Calculator('str')
    with pytest.raises(AssertionError):
        calculator=calc.Calculator([1])
    with pytest.raises(AssertionError):
        calculator=calc.Calculator((1,))

def test_addition_value_type():
    """Tests whether non int or float values can be passed in addition"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.add('str')
    with pytest.raises(AssertionError):
        calculator.add([1])
    with pytest.raises(AssertionError):
        calculator.add((1,))

def test_subtraction_value_type():
    """Tests whether non int or float values can be passed in subtraction"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.subtract('str')
    with pytest.raises(AssertionError):
        calculator.subtract([1])
    with pytest.raises(AssertionError):
        calculator.subtract((1,))

def test_multiplication_value_type():
    """Tests whether non int or float values can be passed in multiplication"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.multiply('str')
    with pytest.raises(AssertionError):
        calculator.multiply([1])
    with pytest.raises(AssertionError):
        calculator.multiply((1,))

def test_division_value_type():
    """Tests whether non int or float values can be passed in division"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.divide('str')
    with pytest.raises(AssertionError):
        calculator.divide([1])
    with pytest.raises(AssertionError):
        calculator.divide((1,))

def test_exponentiation_value_type():
    """Tests whether non int or float values can be passed in exponentiation"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.exponentiate('str')
    with pytest.raises(AssertionError):
        calculator.exponentiate([1])
    with pytest.raises(AssertionError):
        calculator.exponentiate((1,))

def test_root_value_type():
    """Tests whether non int or float values can be passed in taking root"""
    calculator=calc.Calculator()
    with pytest.raises(AssertionError):
        calculator.root('str')
    with pytest.raises(AssertionError):
        calculator.root([1])
    with pytest.raises(AssertionError):
        calculator.root((1,))