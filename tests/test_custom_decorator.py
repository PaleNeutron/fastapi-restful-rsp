from fastapi_restful_rsp.custom_decorator import create_restful_rsp_decorator

def test_create_restful_rsp_decorator():
    # Define test parameters
    data_name = "data"
    message_name = "message"
    param_dict = {"param1": (int, 10), "param2": (str, "default")}
    code_name = "code"

    # Create the decorator
    decorator = create_restful_rsp_decorator(
        data_name=data_name,
        message_name=message_name,
        param_dict=param_dict,
        code_name=code_name,
    )

    # Define a test function
    @decorator
    def test_function(a: str, b: int) -> str:
        return a * b

    # Call the test function
    result = test_function("ab", 3)

    # Assert the result
    assert result.data == "ababab"
    assert result.message == ""
    assert result.param1 == 10
    assert result.param2 == "default"
    assert result.code == 0