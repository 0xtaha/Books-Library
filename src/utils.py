import ast
from .lenums import SupportedDataTypes

def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n

def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def is_json(myjson):
  try:
    ast.literal_eval(myjson)
  except SyntaxError as e:
    return False
  return True


def check_value_type(value : str ) -> int:
        if is_int(value):
            return SupportedDataTypes.INT.value
        elif is_float(value):
            return SupportedDataTypes.FLOAT.value
        elif is_json(value): 
            return SupportedDataTypes.JSON.value
        else:
            return SupportedDataTypes.STRING.value