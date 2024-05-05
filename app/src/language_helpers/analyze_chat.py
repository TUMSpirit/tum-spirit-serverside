from .generate_metadata import generate
from .retrieve_chat import retrieve_chat
from .store_metadata import store_metadata


def analyze_chat():
    message = retrieve_chat()

    print(message)

    metadata = generate(message["content"])

    print(metadata)

    result = store_metadata(message["id"], message["sender_id"], message["timestamp"], metadata)

    return result