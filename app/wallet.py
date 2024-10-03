import os
import json
from ecdsa import SigningKey, SECP256k1
import hashlib

class Wallet:
    def __init__(self, wallet_path='app/wallet_data.json'):
        self.wallet_path = wallet_path
        if os.path.exists(self.wallet_path):
            self.load_wallet()
        else:
            self.create_wallet()

    def create_wallet(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()
        self.balance = 0
        self.save_wallet()
        print(f"New wallet created. Address: {self.address}")

    def load_wallet(self):
        with open(self.wallet_path, 'r') as f:
            data = json.load(f)
            self.private_key = SigningKey.from_string(bytes.fromhex(data['private_key']), curve=SECP256k1)
            self.public_key = self.private_key.get_verifying_key()
            self.address = data['address']
            self.balance = data.get('balance', 0)
            print(f"Wallet loaded. Address: {self.address}")

    def save_wallet(self):
        data = {
            'private_key': self.private_key.to_string().hex(),
            'public_key': self.public_key.to_string().hex(),
            'address': self.address,
            'balance': self.balance
        }
        with open(self.wallet_path, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        sha256 = hashlib.sha256(public_key_bytes).digest()
        ripemd160 = hashlib.new('ripemd160', sha256).digest()
        return ripemd160.hex()

    def sign_message(self, message):
        return self.private_key.sign(message.encode()).hex()

    def get_public_key(self):
        return self.public_key.to_string().hex()

    def update_balance(self, amount):
        self.balance += amount
        self.save_wallet()
