import re

def normalize_email(email):
    if not email:
        return None
    return email.strip().lower()

def normalize_phone(phone):
    if not phone:
        return None
    return re.sub(r"\D", "", str(phone))