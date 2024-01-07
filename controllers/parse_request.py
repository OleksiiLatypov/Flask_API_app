from flask import request


def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """
    try:
        data_dict = request.form.to_dict()
    except Exception as e:
        print(f"Error getting request data: {str(e)}")
        return {}
