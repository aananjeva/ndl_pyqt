from program_codes.list_all_members_response_codes import ListAllMembersResponseCodes


def on_list_all_members_response(msg):
    try:
        response = msg.payload.decode()
        list_all_members_code = ListAllMembersResponseCodes.string_to_enum(response)
        if list_all_members_code in ListAllMembersResponseCodes:
            with open("../mqtt_responses_cached/list_all_members_authorized.csv", "w") as file:
                file.write(str(list_all_members_code))
            return True
        return False

    except Exception as e:
        return False