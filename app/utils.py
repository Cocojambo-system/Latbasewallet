import json
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

def verify_signature(public_key_hex, signature_hex, data):
    try:
        vk = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
        message = json.dumps(data).encode()
        signature = bytes.fromhex(signature_hex)
        return vk.verify(signature, message)
    except BadSignatureError:
        return False
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False
