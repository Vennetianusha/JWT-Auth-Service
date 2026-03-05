from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# create keys folder
os.makedirs("keys", exist_ok=True)

# generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# convert private key to PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# generate public key
public_key = private_key.public_key()

# convert public key to PEM
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# save private key
with open("keys/private.pem", "wb") as f:
    f.write(private_pem)

# save public key
with open("keys/public.pem", "wb") as f:
    f.write(public_pem)

print("RSA keys generated successfully!")