from passlib.context import CryptContext

# Define the password hashing context
# This is used for hashing and verifying passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    """
    return pwd_context.hash(password)


# TODO: Add JWT token generation and validation functions here later,
# integrating with NextAuth.js JWT structure.
