from web3 import Web3
from eth_account import Account
import os

# Connect to the Base network via RPC
BASE_RPC_URL = "https://base-mainnet.public.blastapi.io"  # Replace with the current Base network RPC URL
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

if not web3.isConnected():
    raise ConnectionError("Failed to connect to the Base network. Please check the RPC URL.")

print("Successfully connected to the Base network!")

# Function to create a new wallet
def create_wallet():
    # Generate a random private key
    private_key = Account.create().privateKey.hex()
    account = Account.from_key(private_key)
    address = account.address
    return private_key, address

# Function to check the balance
def get_balance(address):
    balance = web3.eth.get_balance(address)
    # Convert balance from Wei to ETH (or another unit used in the Base network)
    return web3.fromWei(balance, 'ether')

# Function to send a transaction
def send_transaction(private_key, to_address, amount):
    account = Account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    
    # Create the transaction
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': web3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei('50', 'gwei'),  # Set an appropriate gas price
        'chainId': 8453  # Replace with the current chain ID of the Base network
    }
    
    # Sign the transaction
    signed_tx = account.sign_transaction(tx)
    
    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

# Example usage
if __name__ == "__main__":
    print("Creating a new wallet...")
    priv_key, addr = create_wallet()
    print(f"Address: {addr}")
    print(f"Private Key: {priv_key}")
    print("WARNING: Never share your private key!")
    
    # Check balance
    balance = get_balance(addr)
    print(f"Balance of address {addr}: {balance} ETH")
    
    # Example of sending a transaction (uncomment to use)
    # to = "0xRecipientAddressHere"  # Replace with the recipient's address
    # amount = 0.01  # Amount to send
    # tx_hash = send_transaction(priv_key, to, amount)
    # print(f"Transaction sent. Hash: {tx_hash}")
