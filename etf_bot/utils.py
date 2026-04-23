def safe_str(value, fallback="N/A"):
    if value is None or value == "":
        return fallback
    return str(value)