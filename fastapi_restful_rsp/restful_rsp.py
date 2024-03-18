from fastapi_restful_rsp.custom_decorator import create_restful_rsp_decorator

restful_response = create_restful_rsp_decorator(
    data_name="data", message_name="message", param_dict={"status": (str, "success")}
)
