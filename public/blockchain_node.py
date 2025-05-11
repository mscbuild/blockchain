# === Full Blockchain Node ===
from flask import Flask, jsonify, request
from uuid import uuid4
import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError

# Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# Transaction class
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = ""

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def sign_transaction(self, private_key_hex):
        private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        message = json.dumps(self.to_dict(), sort_keys=True).encode()
        self.signature = private_key.sign(message).hex()

    def is_valid(self):
        if self.sender == "SYSTEM":
            return True
        if not self.signature:
            return False
        try:
            public_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            message = json.dumps(self.to_dict(), sort_keys=True).encode()
            return public_key.verify(bytes.fromhex(self.signature), message)
        except (BadSignatureError, Exception):
            return False

# Blockchain class
class Blockchain:
    difficulty = 2
    mining_reward = 50

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            return True
        return False

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        block.hash = computed_hash
        return block

    def mine_pending_transactions(self, miner_address):
        reward_tx = Transaction("SYSTEM", miner_address, Blockchain.mining_reward)
        self.pending_transactions.insert(0, reward_tx)
        block_data = [tx.__dict__ for tx in self.pending_transactions]
        new_block = Block(len(self.chain), time(), block_data, self.get_last_block().hash)
        mined_block = self.proof_of_work(new_block)
        self.chain.append(mined_block)
        self.pending_transactions = []

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def validate_chain_data(self, chain_data):
        return True  # Simple placeholder

    def rebuild_chain_from_data(self, chain_data):
        chain = []
        for block_dict in chain_data:
            block = Block(block_dict['index'],
                          block_dict['timestamp'],
                          block_dict['data'],
                          block_dict['previous_hash'])
            block.hash = block_dict['hash']
            block.nonce = block_dict['nonce']
            chain.append(block)
        return chain

    def resolve_conflicts(self):
        new_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    chain = data['chain']
                    if length > max_length and self.validate_chain_data(chain):
                        new_chain = chain
                        max_length = length
            except Exception:
                continue

        if new_chain:
            self.chain = self.rebuild_chain_from_data(new_chain)
            return True
        return False

# Flask server
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions(node_identifier)
    return jsonify({"message": "New block mined", "chain_length": len(blockchain.chain)}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({"chain": chain_data, "length": len(chain_data)}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400
    tx = Transaction(values['sender'], values['recipient'], values['amount'])
    tx.signature = values['signature']
    if blockchain.add_transaction(tx):
        return jsonify({"message": "Transaction added"}), 201
    else:
        return jsonify({"message": "Invalid transaction"}), 406

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if not nodes:
        return "Error: Please supply a list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    return jsonify({"message": "New nodes have been added", "total_nodes": list(blockchain.nodes)}), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    message = "Chain was replaced" if replaced else "Our chain is authoritative"
    return jsonify({"message": message, "chain": [b.__dict__ for b in blockchain.chain]}), 200

if __name__ == '__main__':
    app.run(port=5000)
