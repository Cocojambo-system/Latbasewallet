from flask import Flask, request, jsonify
from wallet import Wallet
from blockchain import Blockchain, Block
from utils import verify_signature
import json

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain()

@app.route('/address', methods=['GET'])
def get_address():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({'balance': wallet.balance})

@app.route('/send', methods=['POST'])
def send_transaction():
    data = request.get_json()
    recipient = data.get('recipient')
    amount = data.get('amount')
    signature = data.get('signature')

    if not recipient or not amount or not signature:
        return jsonify({'message': 'Insufficient data'}), 400

    transaction = {
        'sender': wallet.address,
        'recipient': recipient,
        'amount': amount
    }

    if not verify_signature(wallet.get_public_key(), signature, transaction):
        return jsonify({'message': 'Invalid signature'}), 400

    blockchain.add_new_transaction(transaction)
    wallet.update_balance(-amount)
    return jsonify({'message': 'Transaction added'}), 201

@app.route('/mine', methods=['GET'])
def mine_block():
    block_index = blockchain.mine()
    if not block_index:
        return jsonify({'message': 'No transactions to mine'}), 400
    return jsonify({'message': f'Block #{block_index} successfully mined'}), 200

if __name__ == '__main__':
    app.run(debug=True)
