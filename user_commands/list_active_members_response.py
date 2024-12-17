from program_codes.list_active_members_response_codes import ListActiveMembersResponseCodes


def on_list_active_members_response(msg):
    try:
        response = msg
        list_active_members_codes = ListActiveMembersResponseCodes.string_to_enum(response)
        if list_active_members_codes in ListActiveMembersResponseCodes:
            with open("mqtt_responses_cached/list_active_members_authorized.csv", "w") as file:
                file.write(str(list_active_members_codes))
            return True
        return False

    except Exception as e:
        return False