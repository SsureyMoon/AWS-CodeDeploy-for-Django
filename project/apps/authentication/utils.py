from rest_framework_jwt.settings import api_settings


def create_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    if user:
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    return None