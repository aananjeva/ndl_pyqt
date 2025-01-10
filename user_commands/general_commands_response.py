from program_codes.general_commands_response_codes import ResponseCodes

def on_general_commands_response(msg):
    try:
        response = msg
        general_commands_code = ResponseCodes.string_to_enum(response)
        if general_commands_code in ResponseCodes:
            with open("mqtt_responses_cached/general_commands_authorized.csv", "w") as file:
                file.write(str(general_commands_code))
            return True
        return False

    except Exception as e:
        return False
