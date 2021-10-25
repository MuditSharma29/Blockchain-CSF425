from hashlib import sha256
import json
import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, request, jsonify
import requests
from authority_nodes import authority_nodes
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


key = rsa.generate_private_key(
    backend=crypto_default_backend(),
    public_exponent=65537,
    key_size=2048
)

private_key = key.private_bytes(
    crypto_serialization.Encoding.PEM,
    crypto_serialization.PrivateFormat.PKCS8,
    crypto_serialization.NoEncryption()
)

def compute_shaHash(text):
    return sha256(text.encode()).hexdigest()

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0,signer=-1):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.signer = signer

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


#{
    # transaction:[]
    #index:5454
    #ts:asfdsafd
    # ph:asfdasfd
    #merkle_hash:sha256(txn)
# }

class Blockchain:
    #PoA algorithm implemented

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []


    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            print("previous_hash == block.previous_hash is false")
            return False

        if not Blockchain.is_valid_proof(block, proof):
            print("not valid proof")
            return False

        block.hash = proof
        print("block.transactions in add_block function = ",block.transactions)
        self.chain.append(block)
        return True

    @staticmethod
    def proof_of_authority(block):
        signer_count = len(authority_nodes)
        block_number = block.index
        signer_index = block_number%signer_count
        block.signer = authority_nodes[signer_index]
        signer_key = compute_shaHash(str(signer_index))
        signed_data = block.compute_hash() + str(signer_key)
        signed_hash = compute_shaHash(signed_data)
        block.hash = signed_hash
        #self port hash added to the computed _hash gives the signed hash of the block.
        return signed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return ((block_hash == block.compute_hash()+str(private_key))|(block_hash != block.compute_hash()))

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Authority.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        print("self.unconfirmed_transactions = ",self.unconfirmed_transactions)
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.ctime(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_authority(new_block)
        
        self.add_block(new_block, proof)
        print("new_block.transactions = ",new_block.transactions)
        self.unconfirmed_transactions = []

        return True


app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()

# the address to other participating members of the network
peers = set()

@app.route('/time', methods=['GET'])
def gettimeofTxn():
    chain_data = []
    timestamp_arr=[]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    for item in chain_data:
        timestamp_arr.append(item["timestamp"])
    jsonString = json.dumps(timestamp_arr)
    return jsonString


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["Customer", "Amount", "Drink"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.ctime()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            print("chain length is =",chain_length)
            # announce the recently mined block to the network
            print("blockchain.last_block = ",blockchain.last_block.transactions)
            announce_new_block(blockchain.last_block)
        return "Block #{} is mined.".format(blockchain.last_block.index)


# endpoint to add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)
    # response_reg_back = requests.post(request.host_url + "/register_node",
    #                          data=json.dumps(node_address[:-4] + str(port)), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        #global blockchain.unconfirmed
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        # if response_reg_back.status_code==200:
        #     #global blockchain.unconfirmed
        #     # update chain and the peers
        #     chain_dump = response_reg_back.json()['chain']
        #     blockchain = create_chain_from_dump(chain_dump)
        #     peers.update(response_reg_back.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code


def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"],
                      block_data["signer"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"],
                  block_data["signer"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = requests.get_json()
    nodes = json.get('nodes')
    
    # return none if node feild is null
    if nodes is None:
        return 'No node', 400
    
    for node in nodes:
        blockchain.add_node(node)

    # give the response for all the connected nodes and display the nodes
    response = {'message' : 'All the nodes are now connected.',
                'total_nodes' : list(blockchain.nodes)}
    
    # http 201 - request has succeeded and has led to the creation of a resource
    return jsonify(response), 201

def consensus():
    """
    Our naive consensus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)



port = 5003
# Uncomment this line if you want to specify the port number in the code
app.run(debug=True, port=port)
print("app running on port :",port)