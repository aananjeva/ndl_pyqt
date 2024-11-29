from program_codes.forgot_password_response_codes import ForgotPasswordResponseCodes
from program_codes.login_response_codes import LoginResponseCodes


def on_forgot_password_response(msg):
    try:
        response = msg.payload.decode()
        forgot_password_code = ForgotPasswordResponseCodes.string_to_enum(response)
        if forgot_password_code in ForgotPasswordResponseCodes:
            with open("mqtt_responses_cached/forgor_password_authorized.csv", "w") as file:
                file.write(str(forgot_password_code))
            return True
        return False

    except Exception as e:
        return False