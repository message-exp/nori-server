from contextvars import ContextVar, Token


class TokenPayloadHolder:
    def __init__(self) -> None:
        self._var: ContextVar = ContextVar("token_payload")

    def set(self, value: dict) -> Token:
        return self._var.set(value)

    def get(self) -> dict:
        return self._var.get(None)


token_payload = TokenPayloadHolder()
