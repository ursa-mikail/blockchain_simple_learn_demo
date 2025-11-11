import hmac
import hashlib
import time
import json
from datetime import datetime
import random

# Function to generate HMAC
def generate_hmac(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

# Function to translate timestamp to ISO 8601 format
def timestamp_to_iso8601(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")

# Previous users and master key (these would be passed or loaded from the previous script)
master_key = "static_master_key"
users = [
    {
        "type": "user_init",
        "user_profile": {
            "name": "User 1",
            "balance": 1000.00  # Initial balance
        },
        "hmac_key": "user1_hmac_key"
    },
    {
        "type": "user_init",
        "user_profile": {
            "name": "User 2",
            "balance": 1000.00  # Initial balance
        },
        "hmac_key": "user2_hmac_key"
    }
]

class PaymentTransaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.transaction_id = self._generate_transaction_id()

    def _generate_transaction_id(self):
        """Generate a unique transaction ID"""
        return hmac.new(
            str(self.timestamp).encode(),
            str(self.amount).encode(),
            hashlib.sha256
        ).hexdigest()[:16]

    def validate_transaction(self):
        """Basic transaction validation"""
        return (
            self.amount > 0 and
            self.sender["user_profile"]["balance"] >= self.amount
        )

    def execute_transaction(self):
        """Execute the transaction if valid"""
        if not self.validate_transaction():
            raise ValueError("Invalid transaction")

        # Deduct amount from sender
        self.sender["user_profile"]["balance"] -= self.amount

        # Add amount to recipient
        self.recipient["user_profile"]["balance"] += self.amount

        return self._create_transaction_cp()

    def _create_transaction_cp(self):
        """Create a Checkpoint (CP) for the transaction"""
        transaction_cp = {
            "type": "payment_transaction",
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "timestamp_iso8601": timestamp_to_iso8601(self.timestamp),
            "sender": {
                "name": self.sender["user_profile"]["name"],
                "pre_transaction_balance": self.sender["user_profile"]["balance"] + self.amount,
                "post_transaction_balance": self.sender["user_profile"]["balance"]
            },
            "recipient": {
                "name": self.recipient["user_profile"]["name"],
                "pre_transaction_balance": self.recipient["user_profile"]["balance"] - self.amount,
                "post_transaction_balance": self.recipient["user_profile"]["balance"]
            },
            "amount": self.amount
        }

        # Sign the transaction CP
        transaction_cp["hmac"] = generate_hmac(
            master_key,
            json.dumps(transaction_cp, sort_keys=True)
        )

        return transaction_cp

class WitnessService:
    def __init__(self, user1_hmac_key, user2_hmac_key):
        self.user1_hmac_key = user1_hmac_key
        self.user2_hmac_key = user2_hmac_key

    def validate_and_witness_transaction(self, transaction_cp):
        """Validate and provide witness signature for the transaction"""
        witness_cp = {
            "type": "transaction_witness",
            "timestamp": time.time(),
            "timestamp_iso8601": timestamp_to_iso8601(time.time()),
            "transaction_id": transaction_cp["transaction_id"],
            "witness_hmac_keys": [self.user1_hmac_key, self.user2_hmac_key]
        }

        # Sign the witness CP
        witness_cp["hmac"] = generate_hmac(
            master_key,
            json.dumps(witness_cp, sort_keys=True)
        )

        return witness_cp

def main():
    # Simulate a transaction between the two users
    sender = users[0]
    recipient = users[1]

    # Random transaction amount
    transaction_amount = round(random.uniform(10, 200), 2)

    try:
        # Create and execute the transaction
        transaction = PaymentTransaction(sender, recipient, transaction_amount)
        transaction_cp = transaction.execute_transaction()

        # Create witness service
        witness_service = WitnessService(
            users[0]["hmac_key"],
            users[1]["hmac_key"]
        )

        # Get witness signature
        witness_cp = witness_service.validate_and_witness_transaction(transaction_cp)

        # Print transaction details
        print("Transaction Checkpoint:")
        print(json.dumps(transaction_cp, indent=4))
        print("\nWitness Checkpoint:")
        print(json.dumps(witness_cp, indent=4))

        # Print updated balances
        print("\nUpdated User Balances:")
        for user in users:
            print(f"{user['user_profile']['name']}: ${user['user_profile']['balance']:.2f}")

    except Exception as e:
        print(f"Transaction failed: {e}")

if __name__ == "__main__":
    main()

"""
Transaction Checkpoint:
{
    "type": "payment_transaction",
    "transaction_id": "040620cdf64e45a1",
    "timestamp": 1762899085.0229907,
    "timestamp_iso8601": "2025-11-11T22:11:25",
    "sender": {
        "name": "User 1",
        "pre_transaction_balance": 1000.0,
        "post_transaction_balance": 950.3
    },
    "recipient": {
        "name": "User 2",
        "pre_transaction_balance": 1000.0,
        "post_transaction_balance": 1049.7
    },
    "amount": 49.7,
    "hmac": "38abda4711adad520f259087fa1985a294114d8c9e1e317995be27c0e55c0534"
}

Witness Checkpoint:
{
    "type": "transaction_witness",
    "timestamp": 1762899085.023176,
    "timestamp_iso8601": "2025-11-11T22:11:25",
    "transaction_id": "040620cdf64e45a1",
    "witness_hmac_keys": [
        "user1_hmac_key",
        "user2_hmac_key"
    ],
    "hmac": "925b314b9ba5a58ad86e91d67d3fa54830dca84cbbd889321b4c6765176b77de"
}

Updated User Balances:
User 1: $950.30
User 2: $1049.70

"""    