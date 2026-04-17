from time import time
import json
import hashlib
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.pending_transactions = []  # Transactions not yet included in a block
        self.chain = []                 # The persistent ledger
        self.nodes = set()              # List of peer nodes in the network

        # Creation of the Genesis Block (the starting point of the chain)
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Adds a new node to the list of known peers.
        :param address: Address of the node (e.g., 'http://127.0.0.1:8000')
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts addresses without a scheme (e.g., '127.0.0.1:8001')
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Validates the integrity of a blockchain.
        Checks if the hashes match and if the Proof of Work is valid for each block.
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            
            # Verify that the block points correctly to the previous one
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Verify that the Proof of Work was performed correctly
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Consensus Algorithm: Resolves conflicts by replacing our local chain
        with the longest valid one found in the network.
        """
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)

        # Contact all neighbor nodes to compare chain lengths
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # The "Longest Chain Rule" - characteristic of Proof of Work systems
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the chain.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Clear the list of pending transactions and append the block
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, id, channel, data, timestamp):
        """
        Creates a new transaction to be added to the next mined block.
        """
        self.pending_transactions.append({
            'id': id,
            'channel': channel,
            'data': data,
            'timestamp': timestamp,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Calculates the SHA-256 hash of a block.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Finds a proof 'p' such that hash(last_p, p) starts with 4 zeros.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validation logic: Does the hash meet the difficulty target (4 leading zeros)?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# =============== FLASK WEB SERVER ===============

app = Flask(__name__)

# Assign a unique identity to this node in the network
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain logic
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Execute Proof of Work to find the next valid block
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Block successfully mined",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Verify that the request contains the necessary transaction data
    required = ['id', 'canale', 'dati', 'timestamp']
    if not all(k in values for k in required):
        return 'Error: Missing transaction data', 400

    index = blockchain.new_transaction(values['id'], values['canale'], values['dati'], values['timestamp'])

    response = {'message': f'Transaction recorded. Expected in Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    # Returns the entire local chain and its length
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    node = values.get('node')

    if node is None:
        return "Error: Provide a valid node URL", 400

    blockchain.register_node(node)

    response = {
        'message': 'Peer node registered successfully',
        'active_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    # Run the consensus protocol to ensure consistency with peers
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Conflict resolved: Local chain updated with the longer version',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Consensus reached: Local chain is already authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    # Node 8003 specifically runs on port 8003
    app.run(host='0.0.0.0', port=8003)
