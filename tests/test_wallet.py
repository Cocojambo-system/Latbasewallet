import unittest
from app.wallet import Wallet

class TestWallet(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet(wallet_path='app/test_wallet.json')

    def test_wallet_creation(self):
        self.assertIsNotNone(self.wallet.private_key)
        self.assertIsNotNone(self.wallet.public_key)
        self.assertIsNotNone(self.wallet.address)

    def test_sign_message(self):
        message = "Test Message"
        signature = self.wallet.sign_message(message)
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 128)  # ECDSA signature of 64 bytes in hex

    def tearDown(self):
        import os
        if os.path.exists('app/test_wallet.json'):
            os.remove('app/test_wallet.json')

if __name__ == '__main__':
    unittest.main()
