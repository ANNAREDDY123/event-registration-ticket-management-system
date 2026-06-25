import uuid


def generate_ticket():

    return str(uuid.uuid4())[:8].upper()
