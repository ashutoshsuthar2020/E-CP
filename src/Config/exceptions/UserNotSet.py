class UserNotSet(Exception):
    def __init__(self) -> None:
        super().__init__("User not set yet")
