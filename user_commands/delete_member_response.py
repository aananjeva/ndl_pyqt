from program_codes.delete_member_response_codes import DeleteMemberResponseCodes

def on_delete_member_response(msg):
    try:
        response = msg.payload.decode()
        delete_member_code = DeleteMemberResponseCodes.string_to_enum(response)
        if delete_member_code in DeleteMemberResponseCodes:
            with open("mqtt_responses_cached/delete_member_authorized.csv", "w") as file:
                file.write(str(delete_member_code))
            return True
        return False

    except Exception as e:
        return False