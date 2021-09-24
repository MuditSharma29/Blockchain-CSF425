from hashlib import sha256
import json
import time

from flask import Flask, request
import requests

def compute_Sha256(input):
    return sha256(input).hexdigest()

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        leafhash = []
        for txn in transactions:
            leafhash.append(compute_Sha256(txn))
        self.leafhash = leafhash

    def compute_merkle_root(self):#calculate the merkle root of the transactions
        print(self.leafhash)

newbclk =  Block(0, [{"author":"neil","price":"50"},{"author":"neil121","price":"5540"}], 0, "0")
print(newbclk.compute_merkle_root())