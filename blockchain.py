import hashlib
import json
from time import time
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS

class Blockchain(object):
	def __init__(self):
		self.chain = []
		self.transactions = []
		self.difficulty = 3
		self.difficulty_check = "0" * self.difficulty

		self.add_genesis_block()

	@property
	def last_block(self):
		return self.chain[-1]

	def add_genesis_block(self):
		block = {
			'index': 1,
			'timestamp': time(),
			'transactions': [],
			'nonce': 0,
			'parent_hash': 'The sky above the port was the color of television, tuned to a dead channel.',
			'hash': self.hash({
				'index': 1,
				'timestamp': time(),
				'transactions': [],
				'nonce': 0,
				'parent_hash': 'The sky above the port was the color of television, tuned to a dead channel.'
				})
		}
		self.chain.append(block)

		return block, True

	def add_block(self, nonce, last_block_hash):
		if (self.check_nonce(nonce) == False):
			return None, False

		if (last_block_hash != self.last_block['hash']):
			return None, False

		block = {
			'index': len(self.chain)+1,
			'timestamp': time(),
			'transactions': self.transactions,
			'nonce': nonce,
			'parent_hash': self.chain[-1]['hash'],
			'hash': self.hash({
				'index': len(self.chain)+1,
				'timestamp': time(),
				'transactions': self.transactions,
				'nonce': nonce,
				'parent_hash': self.chain[-1]['hash'],
				})
		}

		self.transactions = []
		self.chain.append(block)

		return block, True

	def add_transaction(self, transaction_data, public_key, signature):
		if (transaction_data['amount'] <=0):
			print('Invalid amount')
			return None, False

		hash = SHA256.new()
		hash.update(json.dumps(transaction_data, sort_keys=True).encode('utf8'))
		verify = PKCS1_PSS.new(public_key)
		if (verify.verify(hash, signature) == False):
			print('Invalid signature')
			return None, False

		transaction = transaction_data.copy()
		transaction['timestamp'] = time()
		self.transactions.append(transaction)

		return True

	def hash(self, data):
		return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

	def check_nonce(self, nonce):
		last_nonce = self.last_block['nonce']
		last_hash = self.last_block['parent_hash']
		hashed_nonce = hashlib.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())
		return hashed_nonce.hexdigest()[:self.difficulty] == self.difficulty_check

	def mine(self, blockchain):
		nonce = 0
		while not blockchain.check_nonce(nonce):
			nonce += 1
		return nonce

	def sign(self, transaction_data, private_key):
		hash = SHA256.new()
		hash.update(json.dumps(transaction_data, sort_keys=True).encode('utf8'))
		signer = PKCS1_PSS.new(private_key)
		signature = signer.sign(hash)
		return signature


