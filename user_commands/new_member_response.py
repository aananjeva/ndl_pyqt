from program_codes.new_member_response_codes import NewMemberResponseCodes

def on_new_member_response(msg):
    try:
        response = msg.payload.decode()
        new_member_code = NewMemberResponseCodes.string_to_enum(response)
        if new_member_code in NewMemberResponseCodes:
            with open("mqtt_responses_cached/add_member_authorized.csv", "w") as file:
                file.write(str(new_member_code))
            return True
        return False

    except Exception as e:
        return False