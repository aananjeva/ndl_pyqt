import json
from venv import logger

from program_codes.register_response_codes import RegisterResponseCodes

def on_register_response(msg):
    try:
        response = msg
        register_code = RegisterResponseCodes.string_to_enum(response)
        if register_code in RegisterResponseCodes:
            with open("mqtt_responses_cached/register_authorized.csv", "w") as file:
                file.write(str(register_code))
            return True
        return False

    except json.JSONDecodeError:
        logger.debug("Failed to decode the response as JSON.")
        file.write("FAILED")
        return False