from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets

PRIVATE_KEY_PATH = "keys/private.pem"
PUBLIC_KEY_PATH = "keys/public.pem"

ALGORITHM = "RS256"
ISSUER = "jwt-auth-service"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PASSWORD HASH
def hash_password(password: str):
    return pwd_context.hash(password[:72])


# VERIFY PASSWORD
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)


# CREATE ACCESS TOKEN
def create_access_token(username: str):

    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    now = datetime.utcnow()

    payload = {
        "iss": ISSUER,
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=15)).timestamp()),
        "roles": ["user"]
    }

    encoded_jwt = jwt.encode(
        payload,
        private_key,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# VERIFY JWT TOKEN
def verify_token(token: str):

    with open(PUBLIC_KEY_PATH, "r") as f:
        public_key = f.read()

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None


# GENERATE REFRESH TOKEN
def create_refresh_token():
    return secrets.token_hex(32)