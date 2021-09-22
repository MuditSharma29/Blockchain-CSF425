from hashlib import sha256
import json
import time

from flask import Flask, request
import requests


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        # for elements in self.__dict__:
        print(block_string)
        # return sha256(block_string.encode()).hexdigest()

newbclk =  Block(0, [], 0, "0")
print(newbclk.compute_hash())