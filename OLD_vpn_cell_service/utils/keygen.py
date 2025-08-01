from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
import base64

# Генерация пары ключей
private_key = x25519.X25519PrivateKey.generate()
public_key = private_key.public_key()

# Преобразуем в base64 (URL-safe, без padding)
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption(),
)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
)

private_b64 = base64.urlsafe_b64encode(private_bytes).decode().rstrip("=")
public_b64 = base64.urlsafe_b64encode(public_bytes).decode().rstrip("=")

print("Private key (base64):", private_b64)
print("Public key  (base64):", public_b64)
