from flask import request


# TODO: Unnecessary
def current_url(context):
    return request.base_url + request.path
