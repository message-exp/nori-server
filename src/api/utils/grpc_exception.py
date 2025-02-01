import grpc
from typing import Optional

class GrpcException(Exception):
    status_code: grpc.StatusCode = grpc.StatusCode.UNKNOWN
    details: str = 'Unknown exception occurred'

    def __init__(
        self,
        details: Optional[str] = None,
        status_code: Optional[grpc.StatusCode] = None
    ) -> None:
        if status_code is not None:
            if status_code == grpc.StatusCode.OK:
                raise ValueError("The status code for an exception cannot be OK")
            self.status_code = status_code
        if details is not None:
            self.details = details

class PermissionDenied(GrpcException):
    status_code = grpc.StatusCode.PERMISSION_DENIED
    details = "The caller does not have permission to execute the specified operation"

class Unauthenticated(GrpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED
    details = "The request does not have valid authentication credentials for the operation"
