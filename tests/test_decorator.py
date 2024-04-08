from fastapi_restful_rsp.custom_decorator import create_restful_rsp_decorator
from fastapi_restful_rsp import restful_response
from fastapi import Response


async def test_create_restful_rsp_decorator():
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

    @decorator
    async def test_aio_func(a: str, b: int) -> str:
        return a * b

    result = await test_aio_func("ab", 3)
    assert result.data == "ababab"
    assert result.message == ""
    assert result.param1 == 10
    assert result.param2 == "default"
    assert result.code == 0


async def test_304_response():
    @restful_response
    def test_function(a: str, b: int) -> str:
        return Response(status_code=304)

    result = test_function("ab", 3)
    assert result.status_code == 304

    @restful_response
    async def test_aio_func(a: str, b: int) -> str:
        return Response(status_code=304)

    result = await test_aio_func("ab", 3)
    assert result.status_code == 304
