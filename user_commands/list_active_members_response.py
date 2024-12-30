
def on_list_active_members_response(msg):
    try:
        response = msg
        if response:
            with open("mqtt_responses_cached/list_active_members_authorized.csv", "w") as file:
                file.write(str(response))
            return True
        return False

    except Exception as e:
        return False