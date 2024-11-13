# deserialize one item
def individual_serial(message) -> dict:
    return {
        "id": str(message["_id"]),
        "time": message["time"],
        "clientId": message["clientId"],
        "username": message["username"],
        "message": message["message"]
    }

# deserialize all the items
def list_serial(messages) -> list:
    return[individual_serial(message) for message in messages]