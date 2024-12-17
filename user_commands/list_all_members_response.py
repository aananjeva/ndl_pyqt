from program_codes.list_all_members_response_codes import ListAllMembersResponseCodes


def on_list_all_members_response(msg):
    try:
        response = msg
        if response:
            with open("mqtt_responses_cached/list_all_members_authorized.csv", "w") as file:
                file.write(str(response))
            return True
        return False

    except Exception as e:
        return False