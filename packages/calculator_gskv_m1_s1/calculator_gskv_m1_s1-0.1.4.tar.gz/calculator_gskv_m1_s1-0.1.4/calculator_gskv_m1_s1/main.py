class Calculator:
    """
    This class is used to perform simple mathematical operations such as addition, subtraction,
    multiplication, division, exponation, root extraction
    """
    def __init__(self, current_value: float = 0) -> None:
        """Initializes the instance with a default current value of 0"""
        assert isinstance(current_value, (int, float)), (
            f'Cannot accept {type(current_value)} as an argument must be int or float')
        self.current_value=current_value
        return None
    
    def add(self, number_to_add:float) -> float:
        """Add the argument value to the current value"""
        assert isinstance(number_to_add, (int,float)), (
            f'Cannot accept {type(number_to_add)} as an argument must be int or float')
        self.current_value+=number_to_add
        return self.current_value
    
    def subtract(self, number_to_subtract: float) -> float:
        """Subtract the argument value to the current value"""
        assert isinstance(number_to_subtract, (int,float)), (
            f'Cannot accept {type(number_to_subtract)} as an argument must be int or float')
        self.current_value-=number_to_subtract
        return self.current_value
    
    def multiply(self, multiplier:float) ->float:
        """Multiply the current value by argument value"""
        assert isinstance(multiplier, (int,float)), (
            f'Cannot accept {type(multiplier)} as an argument must be int or float')
        self.current_value=self.current_value*multiplier
        return self.current_value

    def divide(self, divisor:float) ->float:
        """Divide the current value by argument value"""
        assert isinstance(divisor, (int,float)), (
            f'Cannot accept {type(divisor)} as an argument must be int or float')
        if divisor == 0:
            raise ValueError('Can not divide by 0')
        self.current_value=self.current_value/divisor
        return self.current_value
        
    def exponentiate(self, exponent:float) ->float:
        """Raises the current value to the power of argument value"""
        """Divide the current value by argument value"""
        assert isinstance(exponent, (int,float)), (
            f'Cannot accept {type(exponent)} as an argument must be int or float')
        self.current_value=self.current_value**exponent
        return self.current_value

    def root(self, root_index:float) ->float:
        """Takes the root of the current value with argument as index"""
        assert isinstance(root_index, (int,float)), (
            f'Cannot accept {type(root_index)} as an argument must be int or float')
        if (root_index % 2) == 0:
            assert self.current_value >= 0,(
                'Imaginary nunbers are not supported, cannot use even root index on negatives')
            self.current_value=self.current_value**(1/root_index)
            return self.current_value
        else:           
            self.current_value=self.current_value**(1/root_index)
            return self.current_value

    def reset(self) ->float:
        """Resets current value to 0"""
        self.current_value=0
        return self.current_value