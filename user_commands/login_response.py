import json

from program_codes.login_response_codes import LoginResponseCodes


def on_login_response(msg: str):
    try:
        response = json.loads(msg)

        code = response.get("code")
        session_token = response.get("session_token")

        login_code = LoginResponseCodes.string_to_enum(code)
        if login_code == LoginResponseCodes.OK:
            with open("mqtt_responses_cached/login_authorized.csv", "w") as file:
                file.write(str(login_code))

            with open("mqtt_responses_cached/session_token", "w") as token_file:
                token_file.write(session_token)

            return True

        return False

    except json.JSONDecodeError:
        print("Failed to decode the response as JSON.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    # i need to read two things: {"code": "OK", "session_token": "f51b6d7709644a45be822bbe33431540"}
    # the code is saved to login_authorized
    # the sssion_token is saved to a file session_token