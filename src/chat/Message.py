from .avatars import *


class Message:
    role: str
    message: str
    avatar: str

    def __init__(self, role, message):
        self.role = role
        self.message = message
        self.avatar = avatars[role]

    def getRole(self) -> str:
        return self.role

    def getMessage(self) -> str:
        return self.message

    def getAvatar(self) -> str:
        return self.avatar

    def toLLMDict(self) -> dict:
        return {"role": self.getRole(), "content": self.message}
