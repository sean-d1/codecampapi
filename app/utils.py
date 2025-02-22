from passlib.context import CryptContext

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pswd_context.hash(password)


def verify(password: str, hashed_password: str) -> bool:
    return pswd_context.verify(password, hashed_password)
