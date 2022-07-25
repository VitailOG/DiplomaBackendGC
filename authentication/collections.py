from beanie import Document


class Message(Document):
    user_id: int
    message: str

    class Settings:
        name = "messages"


__all__ = [
    "Message"
]
