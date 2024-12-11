import re

def validate_transaction_id(transaction_id: str) -> bool:
    """
    Validates transaction ID format.
    Assumes transaction ID should be alphanumeric and at least 6 characters long.
    """
    if not transaction_id:
        return False
    
    pattern = r'^[A-Za-z0-9]{6,}$'
    return bool(re.match(pattern, transaction_id))