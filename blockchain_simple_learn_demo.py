import hashlib
import json
import time
#!pip install faker
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_transaction_history(num_transactions=10, initial_balance=1000.0):
    fake = Faker()
    transactions = []
    balance = initial_balance
    
    for _ in range(num_transactions):
        date = fake.date_time_between(start_date="-1y", end_date="now")
        transaction_id = fake.uuid4()
        description = fake.sentence(nb_words=4)
        amount = round(random.uniform(-500, 500), 2)
        balance += amount
        
        transactions.append({
            "Date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "Transaction ID": transaction_id,
            "Description": description,
            "Amount": amount,
            "Balance": round(balance, 2)
        })
    
    return transactions

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, int(time.time()), data)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()

    for i in range(10):
        transaction_history = generate_transaction_history(1)
        for transaction in transaction_history:
            blockchain.add_block(transaction)

    """
    transaction_history = generate_transaction_history(10)
    for transaction in transaction_history:
        print(transaction)
    """        
    for block in blockchain.chain:
        print(block.__dict__)



"""
{'index': 0, 'previous_hash': '0', 'timestamp': 1739378790, 'data': 'Genesis Block', 'nonce': 0, 'hash': 'ffc43f7e2bf5eb8294aebe03eae9d3e221319e7671a61c3abe9e9b28c9e0f67f'}
{'index': 1, 'previous_hash': 'ffc43f7e2bf5eb8294aebe03eae9d3e221319e7671a61c3abe9e9b28c9e0f67f', 'timestamp': 1739378790, 'data': {'Date': '2024-04-01 09:36:20', 'Transaction ID': '9193da00-1865-4138-bc88-ce0769b631ad', 'Description': 'Different institution issue.', 'Amount': -298.32, 'Balance': 701.68}, 'nonce': 0, 'hash': '482be0311cb52552a2dee800cb99cf536284b33799a56506510d4bf8640eedc2'}
{'index': 2, 'previous_hash': '482be0311cb52552a2dee800cb99cf536284b33799a56506510d4bf8640eedc2', 'timestamp': 1739378790, 'data': {'Date': '2024-06-17 16:58:16', 'Transaction ID': '8e29fbb0-e368-46c2-9527-f3106dd1ae90', 'Description': 'Able TV parent school political.', 'Amount': 23.5, 'Balance': 1023.5}, 'nonce': 0, 'hash': 'b4703f0cb5e34c3471b847a0434b4ef2020565aef9b4baeb555753306b1ebaab'}
{'index': 3, 'previous_hash': 'b4703f0cb5e34c3471b847a0434b4ef2020565aef9b4baeb555753306b1ebaab', 'timestamp': 1739378790, 'data': {'Date': '2024-07-10 21:58:50', 'Transaction ID': '2953e9c5-bb01-4c98-8838-47378c607ad6', 'Description': 'Perform happen late.', 'Amount': -461.85, 'Balance': 538.15}, 'nonce': 0, 'hash': '6eea5f5b72ba72e1b0157adf0d6f7bfe2437e63de33fe7aa23806b6fad6da1c2'}
{'index': 4, 'previous_hash': '6eea5f5b72ba72e1b0157adf0d6f7bfe2437e63de33fe7aa23806b6fad6da1c2', 'timestamp': 1739378790, 'data': {'Date': '2025-01-20 09:55:49', 'Transaction ID': 'd9f87627-1694-42f8-ad13-f93d9402ae6f', 'Description': 'Manager expect program radio.', 'Amount': -125.19, 'Balance': 874.81}, 'nonce': 0, 'hash': 'fd94c0b02d651d986bbf9ebf3bf0a2a3f0b565656245fa63c0dc4085f327ae57'}
{'index': 5, 'previous_hash': 'fd94c0b02d651d986bbf9ebf3bf0a2a3f0b565656245fa63c0dc4085f327ae57', 'timestamp': 1739378790, 'data': {'Date': '2024-10-12 21:29:43', 'Transaction ID': 'f7a10459-c652-4e40-adf9-2afd0fbcdf34', 'Description': 'Social receive source.', 'Amount': 444.58, 'Balance': 1444.58}, 'nonce': 0, 'hash': 'e56d2becec5ae04b35667a2ee08f049d8fca00a8108900e6f03f31dee2943ced'}
{'index': 6, 'previous_hash': 'e56d2becec5ae04b35667a2ee08f049d8fca00a8108900e6f03f31dee2943ced', 'timestamp': 1739378790, 'data': {'Date': '2024-05-22 07:16:18', 'Transaction ID': '87f474ed-c51d-4afa-8a64-834bd388d36e', 'Description': 'Concern move apply religious event.', 'Amount': 242.71, 'Balance': 1242.71}, 'nonce': 0, 'hash': 'f099d9b266101ef03800d2e1188a5b9f550dd77ec43c877895f196a4b391d7fe'}
{'index': 7, 'previous_hash': 'f099d9b266101ef03800d2e1188a5b9f550dd77ec43c877895f196a4b391d7fe', 'timestamp': 1739378790, 'data': {'Date': '2024-06-18 22:59:15', 'Transaction ID': '490736ae-c597-40c8-9ccc-3fef987148e3', 'Description': 'Bed whose me.', 'Amount': 182.71, 'Balance': 1182.71}, 'nonce': 0, 'hash': '0677b5bb38afe23067afee94e379defaf4da0a258f68051a39db82c55439c288'}
{'index': 8, 'previous_hash': '0677b5bb38afe23067afee94e379defaf4da0a258f68051a39db82c55439c288', 'timestamp': 1739378790, 'data': {'Date': '2024-07-22 03:29:29', 'Transaction ID': 'e51074b0-b296-4354-b6a3-bb3c833c4ff5', 'Description': 'Wide PM government.', 'Amount': 330.53, 'Balance': 1330.53}, 'nonce': 0, 'hash': '75dc9834608f858364d7fdb2e9e6f17a42e956ec7ac3f613d6b5b70d120548e3'}
{'index': 9, 'previous_hash': '75dc9834608f858364d7fdb2e9e6f17a42e956ec7ac3f613d6b5b70d120548e3', 'timestamp': 1739378790, 'data': {'Date': '2024-07-01 00:03:05', 'Transaction ID': '96260d66-1e08-43cf-b690-22834c739817', 'Description': 'These born back truth current.', 'Amount': 84.72, 'Balance': 1084.72}, 'nonce': 0, 'hash': '3fdbda1571ca5de8074bdb0294c59eea73bf4554ad73b62d9a919f575e9de94c'}
{'index': 10, 'previous_hash': '3fdbda1571ca5de8074bdb0294c59eea73bf4554ad73b62d9a919f575e9de94c', 'timestamp': 1739378790, 'data': {'Date': '2024-02-27 09:59:00', 'Transaction ID': '37dce6ca-b777-4a2a-83b3-8c092e6a9f1b', 'Description': 'Rest whole it option agency.', 'Amount': -112.74, 'Balance': 887.26}, 'nonce': 0, 'hash': '2b46d42cbaf6511fd2f24489c72d41c90872a3c18b0593c70096f475ac426fe1'}
"""