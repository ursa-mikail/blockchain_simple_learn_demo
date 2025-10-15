# Ethereum uses the uncompressed public key without the 0x04 prefix for address generation

#!pip install ecdsa
#!pip install pysha3
import binascii
#import sha3
import hashlib
import os
import sys
from ecdsa import SigningKey, SECP256k1

def generate_private_key() -> str:
    """Generate a random 256-bit private key in hexadecimal format."""
    return os.urandom(32).hex()

def validate_private_key(private_key_hex: str) -> bool:
    """Validate that the private key is 64 hex characters (32 bytes)."""
    return len(private_key_hex) == 64 and all(c in '0123456789abcdef' for c in private_key_hex.lower())

def derive_address_from_private_key(private_key_hex: str) -> dict:
    """
    Derive Ethereum address from a private key.
    
    Args:
        private_key_hex: 64-character hexadecimal string representing 32-byte private key
    
    Returns:
        Dictionary containing private key, public key, and Ethereum address
    """
    if not validate_private_key(private_key_hex):
        raise ValueError("Private key must be a 64-character hexadecimal string (32 bytes)")
    
    # Convert hex string to bytes
    private_key_bytes = binascii.unhexlify(private_key_hex)
    
    # Generate signing key from private key
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    
    # Get verifying key (public key)
    verifying_key = signing_key.get_verifying_key()
    public_key_bytes = verifying_key.to_string()
    
    # Calculate Ethereum address (last 20 bytes of Keccak-256 hash of public key)
    keccak_hash = hashlib.sha3_256() # sha3.keccak_256()
    keccak_hash.update(public_key_bytes)
    address = keccak_hash.hexdigest()[-40:]  # Last 40 hex characters = 20 bytes
    
    return {
        'signing_key': signing_key,
        'verifying_key': verifying_key,
        'private_key': signing_key.to_string().hex(),
        'public_key': {
            'x': public_key_bytes.hex()[:64],  # First 32 bytes
            'y': public_key_bytes.hex()[64:]   # Last 32 bytes
        },
        'address': address
    }

def sign_message(signing_key: SigningKey, message: str) -> dict:
    """
    Sign a message with the private key.
    
    Args:
        signing_key: The ECDSA signing key object
        message: String message to sign
    
    Returns:
        Dictionary containing signature components and verification result
    """
    message_bytes = message.encode('utf-8')
    signature = signing_key.sign(message_bytes)
    
    # Extract r and s components from the signature
    signature_hex = binascii.hexlify(signature).decode()
    r_component = signature_hex[:64]  # First 32 bytes
    s_component = signature_hex[64:128]  # Next 32 bytes
    
    # Verify the signature
    verifying_key = signing_key.get_verifying_key()
    is_valid = verifying_key.verify(signature, message_bytes)
    
    return {
        'signature_bytes': signature,
        'signature_hex': signature_hex,
        'r': r_component,
        's': s_component,
        'is_valid': is_valid
    }

def main():
    # Option 1: Use the provided private key
    provided_private_key = '3289cccbc9c65fb424a36e726c48ecb7a0f8d8e61dfdff1dc869107978e53ec9'
    
    # Option 2: Generate a random private key (uncomment to use)
    # provided_private_key = generate_private_key()
    
    # Message to sign
    message = 'hello' # "Hello, Ethereum!"
    
    try:
        # Derive address information
        key_info = derive_address_from_private_key(provided_private_key)
        
        # Sign the message
        signature_info = sign_message(key_info['signing_key'], message)
        
        # Display key information
        print(f"Message: {message}\n")
        print(f"Private key: {key_info['private_key']}\n")
        print(f"Public key (x,y): {key_info['public_key']['x']},{key_info['public_key']['y']}\n")
        print(f"Public address: 0x{key_info['address']}\n")
        
        # Display signature information
        print(f"Signature: r={signature_info['r']}, s={signature_info['s']}")
        print(f"Full signature (hex): {signature_info['signature_hex']}")
        print(f"Verify signature: {signature_info['is_valid']}")
        
        # Additional verification for demonstration
        print(f"\n--- Additional Verification ---")
        print(f"Signature length: {len(signature_info['signature_bytes'])} bytes")
        print(f"Using public key to verify: {key_info['verifying_key'].verify(signature_info['signature_bytes'], message.encode())}")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
Message: Hello, Ethereum!

Private key: 3289cccbc9c65fb424a36e726c48ecb7a0f8d8e61dfdff1dc869107978e53ec9

Public key (x,y): 2f3f3f37879e38eb0a4029236452f28996473e93dd816f70fac3df35ab274185,26b92294b0d2c7644152622d5029ef35066ded78c0adc1349a8b642c819c5d65

Public address: 0x9f745e36871cc30906dce32b5ea23299975aeb6a

Signature: r=84cc7174d8af6cbbf5d3e297a0bc105b3cdac667d2e98ff5f6f948473acc33cb, s=34eee441c8143b7b5995eb35b203b90acfcec40a7a8fa36c156449334a925b25
Full signature (hex): 84cc7174d8af6cbbf5d3e297a0bc105b3cdac667d2e98ff5f6f948473acc33cb34eee441c8143b7b5995eb35b203b90acfcec40a7a8fa36c156449334a925b25
Verify signature: True

--- Additional Verification ---
Signature length: 64 bytes
Using public key to verify: True
"""