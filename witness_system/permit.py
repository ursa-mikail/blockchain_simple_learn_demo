import hmac
import hashlib

class PolicyEngine:
    def __init__(self, secret_key):
        self.secret_key = secret_key.encode()

    def create_hmac(self, message):
        message = message.encode()
        return hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

    def verify_hmac(self, message, hmac_to_verify):
        generated_hmac = self.create_hmac(message)
        return hmac.compare_digest(generated_hmac, hmac_to_verify)

    def process_request(self, request):
        # Placeholder for policy processing logic
        # Example: Check if request has a valid HMAC
        if 'hmac' not in request or 'message' not in request:
            return "Invalid request format"

        message = request['message']
        hmac_to_verify = request['hmac']

        if self.verify_hmac(message, hmac_to_verify):
            return "Request is authenticated and processed"
        else:
            return "Authentication failed"

# Example usage
if __name__ == "__main__":
    secret_key = "supersecretkey"
    engine = PolicyEngine(secret_key)

    message = "This is a test message"
    hmac_value = engine.create_hmac(message)
    print(f"Generated HMAC: {hmac_value}")

    request = {
        "message": message,
        "hmac": hmac_value
    }

    result = engine.process_request(request)
    print(result)

    # Test with tampered message
    tampered_request = {
        "message": "This is a tampered message",
        "hmac": hmac_value
    }

    result = engine.process_request(tampered_request)
    print(result)

"""
Generated HMAC: d2b2f5dc72858d07c688eef336cf348c223ff7a418662c90a7e4a739e822a834
Request is authenticated and processed
Authentication failed
"""

# Handle a new permit request
def request_new_permit(user_profile, user_hmac_key):
    new_permit = {
        "type": "new_user_permit",
        "timestamp": time.time(),
        "user_profile": user_profile,
        "hmac_key": user_hmac_key
    }
    new_permit["timestamp_iso8601"] = timestamp_to_iso8601(new_permit["timestamp"])
    new_permit["hmac"] = generate_hmac(master_key, json.dumps(new_permit, sort_keys=True, cls=CustomJSONEncoder))
    return new_permit

# Initial blockchain setup
blockchain = [cp_system] + users

# Create a new user profile using faker
new_user_profile = fake.profile()
new_user_hmac_key = fake.password(length=32)

# Request a new permit
new_user_permit = request_new_permit(new_user_profile, new_user_hmac_key)

# Append the new permit to the blockchain
blockchain.append(new_user_permit)

# Re-sign the entire chain
final_signature = sign_chain(blockchain, master_key)

# Seal the chain into a final CP
final_cp = {
    "type": "final_seal",
    "timestamp": time.time(),
    "blockchain": blockchain,
    "final_signature": final_signature
}
final_cp["timestamp_iso8601"] = timestamp_to_iso8601(final_cp["timestamp"])
final_cp["hmac"] = generate_hmac(master_key, json.dumps(final_cp, sort_keys=True, cls=CustomJSONEncoder))

# Output the updated final CP
print(json.dumps(final_cp, indent=4, cls=CustomJSONEncoder))


"""
{
    "type": "final_seal",
    "timestamp": 1762899308.7960186,
    "blockchain": [
        {
            "type": "system_init",
            "timestamp": 1762898754.4905171,
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "a6ef6b39a1eac8a8aaedadb940fe0f987170cd868346461c51a6f5884dedb402"
        },
        {
            "type": "user_init",
            "user_profile": {
                "name": "User 1",
                "balance": 950.3
            },
            "hmac_key": "user1_hmac_key"
        },
        {
            "type": "user_init",
            "user_profile": {
                "name": "User 2",
                "balance": 1049.7
            },
            "hmac_key": "user2_hmac_key"
        },
        {
            "type": "new_user_permit",
            "timestamp": 1762899308.7956705,
            "user_profile": {
                "job": "Estate agent",
                "company": "Lynn Inc",
                "ssn": "256-87-4723",
                "residence": "972 Kelly Roads Suite 995\nLindseyburgh, UT 06762",
                "current_location": [
                    "-78.9686335",
                    "-111.111974"
                ],
                "blood_group": "A+",
                "website": [
                    "https://robertson.info/",
                    "http://martinez.com/",
                    "http://hall.com/",
                    "https://www.fischer.com/"
                ],
                "username": "rhondacasey",
                "name": "Keith Fisher",
                "sex": "M",
                "address": "09180 Nelson Prairie Suite 012\nWest Martha, WI 32660",
                "mail": "larryliu@yahoo.com",
                "birthdate": "1995-03-09"
            },
            "hmac_key": "qA*zApLJkcy81hXv+nhZs9rSu@v0LgtG",
            "timestamp_iso8601": "2025-11-11T22:15:08",
            "hmac": "f7a6eb3d7093782df727ee69004598d727ed60c8ad9a10b5ae68dc01ef0efa74"
        }
    ],
    "final_signature": "2dba8b531187a138e9711bc90bd55945e5e295386984bce2abaa8bd1067c1590",
    "timestamp_iso8601": "2025-11-11T22:15:08",
    "hmac": "a057152871aab1ebb9e393906121b585dbb2d3ac449756ee3cbf36cc78a049e8"
}

"""