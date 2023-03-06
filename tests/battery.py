def test_exact(expected_result, test_function, params, verbose:bool) -> bool:
    if params:
        result = test_function(params)
    else:
        result = test_function()
    
    if result == expected_result:
        if verbose:
            print("-- Successful Test --")
            print(f"Expected Result: {expected_result} -> Actual: {result} // Function Name: {test_function.__name__}")
        return True
    else:
        if verbose:
            print("-- Unsuccessful Test --")
            print(f"Expected Result: {expected_result} -> Actual: {result} // Function Name: {test_function.__name__}")
        return False

def test_range(expected_result, test_function, params, verbose:bool) -> bool:
    if params:
        result = test_function(params)
    else:
        result = test_function()
    if expected_result['inclusive']:
        if result >= expected_result['min'] and result <= expected_result['max']:
            if verbose:
                print("-- Successful Test --")
                print(f"Minimum: {expected_result['min']} - Maximum: {expected_result['max']} -> Actual: {result} // Function Name: {test_function.__name__}")    
            return True
    else:
        if result > expected_result['min'] and result < expected_result['max']:
            if verbose:
                print("-- Unsuccessful Test --")
                print(f"Minimum: {expected_result['min']} - Maximum: {expected_result['max']} -> Actual: {result} // Function Name: {test_function.__name__}")
            return False