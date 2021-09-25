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
        self.leafhash = self.clone_transactions_for_leafhash()

    #def hash(block):
    #    """
    #    Creates a SHA-256 hash of a Block

    #    :param block: Block
     #   """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    #    block_string = json.dumps(block, sort_keys=True).encode()
     #   return hashlib.sha256(block_string).hexdigest()
    
    """
    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()
    """

    
    def clone_transactions_for_leafhash(self):
        leafhash=[]
        for txn in self.transactions:
            print(txn)
            txn_string = json.dumps(txn, sort_keys=True)
            leafhash.append(compute_Sha256(txn_string.encode()))
            # print(leafhash)
        return leafhash

    def compute_merkle_root(self):#calculate the merkle root of the transactions
        print("new recurssion")
        if len(self.leafhash)!=1:
            if len(self.leafhash)%2==0:
                j=0
                for i in range(0,len(self.leafhash)-1,2):
                    hash_string = json.dumps(self.leafhash[i]+self.leafhash[i+1], sort_keys=True)
                    self.leafhash[j] = compute_Sha256(hash_string.encode())
                    i+=1
                    j+=1
                    print("i = ",i," j = ",j)
                print("self.leafhash = ",self.leafhash)
                self.compute_merkle_root()
            else:
                self.leafhash.append(self.leafhash[len(self.leafhash)-1])
                self.compute_merkle_root()
        else:
            return self.leafhash[0]
            
        

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
def compute_Sha256(input):
    input = input
    return sha256(input).hexdigest()


newbclk =  Block(0, [{"author":"neil","price":"50"},{"author":"neil121","price":"5540"}], 0, "0")

# print(newbclk.compute_merkle_root())

# for i in range(0,10,2):
#     print(i)



arr = [
        {
            "index": 0,
            "transactions": [],
            "timestamp": 0,
            "previous_hash": "0",
            "nonce": 0,
            "hash": "6dbf23122cb5046cc5c0c1b245c75f8e43c59ca8ffeac292715e5078e631d0c9"
        },
        {
            "index": 1,
            "transactions": [
                {
                    "Customer": "vaibhav",
                    "Amount": "500",
                    "Drink": "Frappe",
                    "timestamp": 1632565628.5945456
                },
                {
                    "Customer": "vaibhav",
                    "Amount": "500",
                    "Drink": "Frappe",
                    "timestamp": 1632565630.1936157
                },
                {
                    "Customer": "vaibhav",
                    "Amount": "500",
                    "Drink": "Frappe",
                    "timestamp": 1632565630.893342
                }
            ],
            "timestamp": 1632565633.4045808,
            "previous_hash": "6dbf23122cb5046cc5c0c1b245c75f8e43c59ca8ffeac292715e5078e631d0c9",
            "nonce": 378,
            "hash": "00b155dd2aeb4dfbfb8f1ad23b6c7c573262fcbbf80d80f49c670f20068f18de"
        }
    ]
for i in arr:
    print(i["timestamp"])