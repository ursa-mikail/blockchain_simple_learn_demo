System that creates a blockchain-like structure for tracking system initialization, user registration, and witness verification with HMAC-based integrity protection.

Overview
This system generates a series of cryptographically linked checkpoints (CPs) that document the initialization of a secure system, including payment services, user registration, and witness services. Each checkpoint is timestamped and HMAC-signed to ensure data integrity.

Features
```
Hierarchical Checkpoint Structure: Creates a chain of system initialization events

HMAC Integrity Protection: Each checkpoint is signed with SHA-256 HMAC

Timestamping: Dual timestamp format (Unix timestamp + ISO 8601)

Fake Data Generation: Uses Faker library to generate realistic test data

Blockchain-like Sealing: Final checkpoint seals the entire chain with a master signature
```

1. System Initialization (system_init)
Initializes the core system

Contains system timestamp

Signed with master key

2. Payment Service Initialization (payment_service_init)
Sets up payment services

Contains service initialization timestamp

Signed with master key

3. User Initialization (user_init)
Registers new users with generated profiles

Includes:

User profile (name, contact info, etc.)

Unique HMAC key for each user

Individual timestamps

Signed with master key

4. Witness Initialization (witness_init)
Acts as verification service

Stores HMAC keys of registered users

Provides witness functionality

Signed with master key

5. Final Seal (final_seal)
Seals the entire checkpoint chain

Contains complete blockchain structure

Includes final HMAC signature of entire chain

Provides overall system integrity

Data Structure
```
Each checkpoint contains:

type: Checkpoint category

timestamp: Unix timestamp

timestamp_iso8601: Human-readable ISO 8601 format

hmac: SHA-256 HMAC signature

Type-specific data (user profiles, HMAC keys, etc.)
```

Security Features
```
Static Master Key: Central key for system-wide signatures

Individual User Keys: Unique HMAC keys for each user

Chain Integrity: Final signature validates entire checkpoint chain

Timestamp Verification: Dual-format timestamps prevent tampering
```

## Payment Transaction System
A secure payment processing system that implements blockchain-inspired checkpoints for transaction validation, execution, and witness verification with HMAC-based integrity protection.

Overview
This system extends the checkpoint framework to handle financial transactions between users, providing complete audit trails, balance tracking, and cryptographic verification at each step.

Features
Secure Transaction Processing: Validates and executes payments between users

HMAC Integrity Protection: All checkpoints are signed with SHA-256 HMAC

Witness Verification: Independent witness service validates transactions

Balance Tracking: Real-time balance updates with pre/post transaction states

Transaction Audit Trail: Complete history of all transaction details

Unique Transaction IDs: Cryptographically generated transaction identifiers

Components
1. PaymentTransaction Class
Handles the core transaction logic:

Transaction Validation: Ensures sufficient funds and valid amounts

Balance Updates: Atomically transfers funds between accounts

Checkpoint Generation: Creates signed transaction records

ID Generation: Creates unique transaction identifiers using HMAC

2. WitnessService Class
Provides independent transaction verification:

Multi-key Witnessing: Uses both users' HMAC keys for verification

Transaction Linking: References the original transaction ID

Independent Timestamping: Provides separate verification timing

3. Checkpoint Types
Transaction Checkpoint (payment_transaction)

```
{
  "type": "payment_transaction",
  "transaction_id": "unique_id",
  "sender": {
    "name": "User 1",
    "pre_transaction_balance": 1000.00,
    "post_transaction_balance": 850.00
  },
  "recipient": {
    "name": "User 2", 
    "pre_transaction_balance": 1000.00,
    "post_transaction_balance": 1150.00
  },
  "amount": 150.00,
  "hmac": "signature"
}
```

Witness Checkpoint (transaction_witness)

```
{
  "type": "transaction_witness", 
  "transaction_id": "unique_id",
  "witness_hmac_keys": ["key1", "key2"],
  "hmac": "signature"
}
```

## Policy Engine & Permit System
A comprehensive security framework that combines HMAC-based policy enforcement with a blockchain-inspired permit system for user management and transaction processing.

Overview
This system provides two main components:

Policy Engine: HMAC-based authentication and request validation

Permit System: Blockchain-style user registration and transaction management

Components
1. Policy Engine
A robust HMAC-based authentication system for securing API requests and transactions.

Features:
HMAC Generation: Creates SHA-256 HMAC signatures for messages

Signature Verification: Securely validates incoming requests

Tamper Detection: Identifies modified messages using cryptographic comparison

Request Processing: Handles authenticated requests with policy logic

Usage Example:
```
secret_key = "supersecretkey"
engine = PolicyEngine(secret_key)

# Create HMAC for a message
message = "This is a test message"
hmac_value = engine.create_hmac(message)

# Verify request
request = {"message": message, "hmac": hmac_value}
result = engine.process_request(request)  # "Request is authenticated and processed"
```


2. Permit System
Extends the blockchain checkpoint system to handle user registration and transaction management.

- Checkpoint Types:
System Initialization (system_init)

Bootstraps the entire system

Signed with master key

- User Initialization (user_init)

Registers users with profiles and balances

Includes individual HMAC keys

- New User Permit (new_user_permit)

Dynamic user registration system

Generates realistic user profiles using Faker

Creates unique HMAC keys for each user

Timestamped and cryptographically signed

- Final Seal (final_seal)

Cryptographically seals the entire blockchain

Contains complete transaction history

Provides integrity verification for the entire system

### Integration Workflow
User Registration Flow:

```
# 1. Create new user profile
new_user_profile = fake.profile()
new_user_hmac_key = fake.password(length=32)

# 2. Generate permit request
new_user_permit = request_new_permit(new_user_profile, new_user_hmac_key)

# 3. Add to blockchain
blockchain.append(new_user_permit)

# 4. Re-sign entire chain
final_signature = sign_chain(blockchain, master_key)

# 5. Create final sealed checkpoint
final_cp = create_final_seal(blockchain, final_signature)
```

### Transaction Processing:

```
# Using Policy Engine for transaction authentication
transaction_request = {
    "message": json.dumps(transaction_data),
    "hmac": generated_hmac
}

result = policy_engine.process_request(transaction_request)
if "authenticated" in result:
    process_transaction(transaction_data)

```

### Cryptographic Protection:
Master Key: Signs system-level checkpoints and final seals

User HMAC Keys: Individual keys for user-specific operations

Chain Signing: Each modification re-signs the entire blockchain

Timestamp Verification: ISO 8601 and Unix timestamp formats

### Policy Engine:
Extend process_request() with custom business logic

Add multiple secret keys for different security zones

Implement key rotation policies

### Permit System:
Modify user profile fields as needed

Adjust HMAC key complexity requirements

Add additional checkpoint types for specific operations

### Dependencies
hmac, hashlib: Cryptographic operations

json: Data serialization

datetime, time: Timestamp handling

faker: Test data generation (for demo purposes)

