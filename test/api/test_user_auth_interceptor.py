import pytest
import grpc
import jwt
from typing import Generator, Any
from src.api.user_auth_interceptor import UserAuthInterceptor, auth_config
from src.utils.token_context import token_payload

# Pseudocode:
# 1. Import necessary modules and the interceptor.
# 2. Create a dummy handler call details class with attributes:
#    - method
#    - invocation_metadata (a list of tuples)
# 3. Define a fake continuation function that returns a distinct marker.
# 4. Write tests:
#    a. Test when method does not require authentication:
#       - Use a method not in auth_config.
#       - Assert that the continuation is called.
#    b. Test when method requires auth but no token is provided:
#       - Add an entry in auth_config for a test method.
#       - Create handler details with no 'authorization' metadata.
#       - Assert that interceptor returns the abortion handler.
#    c. Test when a valid token is provided:
#       - Add an entry in auth_config for a test method.
#       - Monkeypatch get_token to return a dummy payload.
#       - Spy on token_payload.set by capturing the payload.
#       - Assert that the continuation is called and token_payload is set.
#    d. Test when jwt.ExpiredSignatureError is raised:
#       - Add an entry in auth_config for a test method.
#       - Monkeypatch get_token to raise jwt.ExpiredSignatureError.
#       - Assert that interceptor returns the abortion handler.
#    e. Test when jwt.InvalidTokenError is raised:
#       - Add an entry in auth_config for a test method.
#       - Monkeypatch get_token to raise jwt.InvalidTokenError.
#       - Assert that interceptor returns the abortion handler.
#
# 5. Restore auth_config modifications if necessary.


# Dummy handler call details for testing
class FakeHandlerCallDetails:
    def __init__(self, method: str, metadata: list) -> None:
        # metadata should be a list of tuples [(key, value)]
        self.method = method
        self.invocation_metadata = metadata


# Dummy continuation function that returns a marker.
def fake_continuation(handler_call_details: grpc.HandlerCallDetails) -> str:
    return "continued"


# A fixture to clean up auth_config modifications after tests.
@pytest.fixture(autouse=True)
def restore_auth_config() -> Generator[None, Any, None]:
    orig_auth_config = auth_config.copy()
    yield
    auth_config.clear()
    auth_config.update(orig_auth_config)


def test_no_auth_required() -> None:
    # Use a method not in auth_config.
    method = "/not/required"
    handler_details = FakeHandlerCallDetails(method, [])
    interceptor = UserAuthInterceptor()

    result = interceptor.intercept_service(fake_continuation, handler_details)
    # Should call continuation because no auth required.
    assert result == "continued"


def test_missing_token() -> None:
    # Set a method which requires auth.
    test_method = "/test/missing_token"
    auth_config[test_method] = True
    handler_details = FakeHandlerCallDetails(
        test_method, []
    )  # No authorization metadata.
    interceptor = UserAuthInterceptor()

    result = interceptor.intercept_service(fake_continuation, handler_details)
    # Expect the abortion handler because token is missing.
    assert result == interceptor._abortion


def test_valid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    # Set a method which requires auth.
    test_method = "/test/valid_token"
    auth_config[test_method] = True
    dummy_payload = {"sub": "test_user"}
    # Replace get_token to return dummy_payload.
    monkeypatch.setattr(
        "src.api.user_auth_interceptor.get_token", lambda token: dummy_payload
    )

    # Spy on token_payload.set
    token_container = {}

    def fake_set(payload: dict) -> None:
        token_container["payload"] = payload

    monkeypatch.setattr(token_payload, "set", fake_set)

    # Provide a valid token in metadata.
    handler_details = FakeHandlerCallDetails(
        test_method, [("authorization", "valid_token")]
    )
    interceptor = UserAuthInterceptor()

    result = interceptor.intercept_service(fake_continuation, handler_details)
    # Expect the continuation to be called.
    assert result == "continued"
    # Ensure token_payload.set was called with dummy_payload.
    assert token_container.get("payload") == dummy_payload


def test_expired_token(monkeypatch: pytest.MonkeyPatch) -> None:
    # Set a method which requires auth.
    test_method = "/test/expired_token"
    auth_config[test_method] = True
    # Replace get_token to raise jwt.ExpiredSignatureError.
    monkeypatch.setattr(
        "src.api.user_auth_interceptor.get_token",
        lambda token: (_ for _ in ()).throw(jwt.ExpiredSignatureError),
    )

    handler_details = FakeHandlerCallDetails(
        test_method, [("authorization", "expired_token")]
    )
    interceptor = UserAuthInterceptor()

    result = interceptor.intercept_service(fake_continuation, handler_details)
    # Expect the abortion handler due to token expiration.
    assert result == interceptor._abortion


def test_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    # Set a method which requires auth.
    test_method = "/test/invalid_token"
    auth_config[test_method] = True
    # Replace get_token to raise jwt.InvalidTokenError.
    monkeypatch.setattr(
        "src.api.user_auth_interceptor.get_token",
        lambda token: (_ for _ in ()).throw(jwt.InvalidTokenError),
    )

    handler_details = FakeHandlerCallDetails(
        test_method, [("authorization", "invalid_token")]
    )
    interceptor = UserAuthInterceptor()

    result = interceptor.intercept_service(fake_continuation, handler_details)
    # Expect the abortion handler due to invalid token.
    assert result == interceptor._abortion
