from fastapi import HTTPException, status

class BusinessLogicError(Exception):
    """Raised when business logic rules are violated"""
    pass

class ValidationError(Exception):
    """Raised when data validation fails"""
    pass

class NotFoundError(Exception):
    """Raised when a requested resource is not found"""
    pass

class PermissionError(Exception):
    """Raised when user lacks required permissions"""
    pass

class DuplicateResourceError(Exception):
    """Raised when trying to create a duplicate resource"""
    pass

class InsufficientFundsError(Exception):
    """Raised when there are insufficient funds for a transaction"""
    pass

class InvalidTransactionError(Exception):
    """Raised when a transaction is invalid"""
    pass

class AccountInactiveError(Exception):
    """Raised when trying to use an inactive account"""
    pass

class CircularReferenceError(Exception):
    """Raised when a circular reference is detected"""
    pass

class InvalidDateRangeError(Exception):
    """Raised when date range is invalid"""
    pass

class InvalidAmountError(Exception):
    """Raised when amount is invalid"""
    pass

# HTTP Exception handlers
def handle_business_logic_error(exc: BusinessLogicError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_validation_error(exc: ValidationError):
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc)
    )

def handle_not_found_error(exc: NotFoundError):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc)
    )

def handle_permission_error(exc: PermissionError):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc)
    )

def handle_duplicate_resource_error(exc: DuplicateResourceError):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc)
    )

def handle_insufficient_funds_error(exc: InsufficientFundsError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_invalid_transaction_error(exc: InvalidTransactionError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_account_inactive_error(exc: AccountInactiveError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_circular_reference_error(exc: CircularReferenceError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_invalid_date_range_error(exc: InvalidDateRangeError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

def handle_invalid_amount_error(exc: InvalidAmountError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )
