import json
import os
from Crypto.PublicKey import RSA
from blockchain import Blockchain

# This is a test case for creating a blockchain with python.
# Alice wishes to send Eric some amount.  
# She signs the transaction and adds it to the blockchain.

# Create the public and private keys for Alice
if os.path.isfile('./keys/private_key.pem'):
	with open('./keys/private_key.pem') as f:
		private_key = RSA.importKey(f.read())
else:
	private_key = RSA.generate(2048)
	with open('./keys/private_key.pem','wb') as f:
		f.write(private_key.exportKey('PEM'))
public_key = private_key.publickey()

# Create the transactions and add to the blockchain
blockchain = Blockchain()

first_transaction = {
	'sender': 'Alice',
	'recipient': 'Eric',
	'amount': 3
}

signature = blockchain.sign(first_transaction, private_key)
blockchain.add_transaction(first_transaction, public_key, signature)

nonce = blockchain.mine(blockchain)
last_block_hash = blockchain.last_block['hash']
blockchain.add_block(nonce, last_block_hash)

second_transaction = {
	'sender': 'Alice',
	'recipient': 'Eric',
	'amount': 20
}

third_transaction = {
	'sender': 'Alice',
	'recipient': 'Eric',
	'amount': 55
}

signature = blockchain.sign(second_transaction, private_key)
blockchain.add_transaction(second_transaction, public_key, signature)

signature = blockchain.sign(third_transaction, private_key)
blockchain.add_transaction(third_transaction, public_key, signature)

last_block_hash = blockchain.last_block['hash']
nonce = blockchain.mine(blockchain)
blockchain.add_block(nonce, last_block_hash)

print(json.dumps(blockchain.chain, indent=4))
