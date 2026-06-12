import uuid


def generate_trace_id():

    return str(
        uuid.uuid4()
    )


def generate_event_id():

    return str(
        uuid.uuid4()
    )