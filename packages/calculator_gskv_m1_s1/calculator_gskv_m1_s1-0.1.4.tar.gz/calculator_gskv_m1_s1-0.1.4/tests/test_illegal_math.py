import calculator_gskv_m1_s1 as calc
import pytest

def test_division_by_zero():
    """Tests wheter division by 0 raises an error"""
    calculator=calc.Calculator()
    with pytest.raises(ValueError):
        calculator.divide(0)

def test_imaginary_root_outcomes():
    """Tests wheter root from a negative with even root index raises an error"""
    calculator=calc.Calculator(-4)
    with pytest.raises(AssertionError):
        calculator.root(2)
