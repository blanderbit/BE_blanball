import uuid


def generate_unique_request_id() -> str:
    return str(uuid.uuid4())
