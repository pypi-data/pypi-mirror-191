def check(value, message, _, **info):
    value = str(value)
    if len(value) == 0:
        return message.clear(f"Please enter a value! ({info.get('info')}")
    return value in info.get("info")
