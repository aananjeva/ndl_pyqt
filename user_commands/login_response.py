from program_codes.login_response_codes import LoginResponseCodes


def on_login_response(msg: str):
    try:
        login_code = LoginResponseCodes.string_to_enum(msg)
        if login_code in LoginResponseCodes:
            with open("mqtt_responses_cached/login_authorized.csv", "w") as file:
                file.write(str(login_code))
            return True
        return False

    except Exception as e:
        return False