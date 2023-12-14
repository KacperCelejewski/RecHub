from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from flask import jsonify, make_response, request


class representative_required:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"] != "company_representative":
            return make_response(
                jsonify({"message": "You are not a representative!"}), 401
            )
        return self.func(*args, **kwargs)
