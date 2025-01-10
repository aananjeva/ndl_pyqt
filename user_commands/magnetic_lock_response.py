from program_codes.magnetic_lock_response_codes import MagneticLockResponseCodes

def on_magnetic_lock_response(msg):
    try:
        response = msg
        magnetic_lock_code = MagneticLockResponseCodes.string_to_enum(response)
        if magnetic_lock_code in MagneticLockResponseCodes:
            with open("mqtt_responses_cached/magnetic_lock_authorized.csv", "w") as file:
                file.write(str(magnetic_lock_code))
            return True
        return False

    except Exception as e:
        return False