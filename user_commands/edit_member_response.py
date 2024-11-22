from program_codes.edit_member_response_codes import EditMemberResponseCodes

def on_edit_member_response(msg):
    try:
        response = msg.payload.decode()
        edit_member_code = EditMemberResponseCodes.string_to_enum(response)
        if edit_member_code in EditMemberResponseCodes:
            with open("../mqtt_responses_cached/edit_member_authorized.csv", "w") as file:
                file.write(str(edit_member_code))
            return True
        return False

    except Exception as e:
        return False