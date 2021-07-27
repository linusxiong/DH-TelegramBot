def return_error(code):
    error_code = {
        1000: {'code': 1000, 'message': "An error occurred"},
        1001: {'code': 1001, 'message': "Database is established"},
        1002: {'code': 1002, 'message': "Table is establish"},
        1003: {'code': 1003, 'message': "Data already exists"},
        1004: {'code': 1004, 'message': "Request error"},
        1005: {'code': 1005, 'message': "URL is invalid"},
        1006: {'code': 1006, 'message': "Timeout"}
    }

    return error_code.get(code, 1000)
