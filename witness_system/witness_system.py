#!pip install faker
import hmac
import hashlib
import time
from datetime import datetime, date
from faker import Faker
import json
from decimal import Decimal
from faker.providers import profile

# Custom JSON Encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Decimal, datetime, date)):
            return str(obj)
        return super().default(obj)

fake = Faker()

# Function to translate timestamp to ISO 8601 format
def timestamp_to_iso8601(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")

# Function to generate HMAC
def generate_hmac(key, message):
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

# Initialize static master key
master_key = "static_master_key"

# Generate initial CP for system configuration
cp_system = {
    "type": "system_init",
    "timestamp": time.time()
}
cp_system["timestamp_iso8601"] = timestamp_to_iso8601(cp_system["timestamp"])
cp_system["hmac"] = generate_hmac(master_key, json.dumps(cp_system, sort_keys=True, cls=CustomJSONEncoder))

# Generate CP for payment service initialization
cp_payment_service = {
    "type": "payment_service_init",
    "timestamp": time.time()
}
cp_payment_service["timestamp_iso8601"] = timestamp_to_iso8601(cp_payment_service["timestamp"])
cp_payment_service["hmac"] = generate_hmac(master_key, json.dumps(cp_payment_service, sort_keys=True, cls=CustomJSONEncoder))

# Generate CPs for two users
users = []
for i in range(2):
    profile = fake.profile()
    hmac_key = fake.password(length=32)
    cp_user = {
        "type": "user_init",
        "timestamp": time.time(),
        "user_profile": profile,
        "hmac_key": hmac_key
    }
    cp_user["timestamp_iso8601"] = timestamp_to_iso8601(cp_user["timestamp"])
    cp_user["hmac"] = generate_hmac(master_key, json.dumps(cp_user, sort_keys=True, cls=CustomJSONEncoder))
    users.append(cp_user)

# Generate CP for service to act as witness
cp_witness = {
    "type": "witness_init",
    "timestamp": time.time(),
    "witness_hmac_keys": [users[0]["hmac_key"], users[1]["hmac_key"]]
}
cp_witness["timestamp_iso8601"] = timestamp_to_iso8601(cp_witness["timestamp"])
cp_witness["hmac"] = generate_hmac(master_key, json.dumps(cp_witness, sort_keys=True, cls=CustomJSONEncoder))

# Chain CPs into a blockchain-like structure
blockchain = [cp_system, cp_payment_service] + users + [cp_witness]

# Function to sign the entire chain with the master key
def sign_chain(chain, master_key):
    chain_data = json.dumps(chain, sort_keys=True, cls=CustomJSONEncoder)
    return generate_hmac(master_key, chain_data)

# Sign the entire chain
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

# Output the final CP
print(json.dumps(final_cp, indent=4, cls=CustomJSONEncoder))

"""
{
    "type": "final_seal",
    "timestamp": 1762898754.515864,
    "blockchain": [
        {
            "type": "system_init",
            "timestamp": 1762898754.4905171,
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "a6ef6b39a1eac8a8aaedadb940fe0f987170cd868346461c51a6f5884dedb402"
        },
        {
            "type": "payment_service_init",
            "timestamp": 1762898754.4910295,
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "9bcca23975d229bcf273cab1c1d83e85c8c8142521a3e85d17deeea1184b9e2d"
        },
        {
            "type": "user_init",
            "timestamp": 1762898754.5031905,
            "user_profile": {
                "job": "Learning mentor",
                "company": "Farrell, Bennett and Smith",
                "ssn": "327-25-7235",
                "residence": "464 Kristen Rapids\nKochview, IL 89144",
                "current_location": [
                    "22.940096",
                    "99.920385"
                ],
                "blood_group": "B+",
                "website": [
                    "https://cross-davis.com/"
                ],
                "username": "espinozapatrick",
                "name": "Matthew Shields",
                "sex": "M",
                "address": "32401 Saunders Key\nLake Robert, AS 19390",
                "mail": "josephblake@yahoo.com",
                "birthdate": "2012-05-27"
            },
            "hmac_key": "p26Pq8GJ07d52!DQGDWLQ2tA#oh(D1&H",
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "4bf3bedcfc72c5f76c85293a95538a23629960bf986f61252087daf47105d6d1"
        },
        {
            "type": "user_init",
            "timestamp": 1762898754.5146813,
            "user_profile": {
                "job": "Intelligence analyst",
                "company": "Rodriguez-Humphrey",
                "ssn": "626-53-1541",
                "residence": "26371 Clay Crescent\nChristopherchester, ND 40709",
                "current_location": [
                    "-49.0087925",
                    "149.400925"
                ],
                "blood_group": "B-",
                "website": [
                    "http://www.hill.com/",
                    "https://jackson.info/",
                    "https://gilmore.org/"
                ],
                "username": "danielsluke",
                "name": "Mrs. Stacy Smith MD",
                "sex": "F",
                "address": "9988 Taylor Avenue Apt. 173\nNorth Erinland, SD 35650",
                "mail": "jlove@gmail.com",
                "birthdate": "2004-04-09"
            },
            "hmac_key": "##u)gtxZD^2L(cghKc(LvN9VeA2D&ATP",
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "027f8ff5ddb3bbf7b73e47cff058abd014cfb56e7e1dca8598a89a3497b04693"
        },
        {
            "type": "witness_init",
            "timestamp": 1762898754.5150514,
            "witness_hmac_keys": [
                "p26Pq8GJ07d52!DQGDWLQ2tA#oh(D1&H",
                "##u)gtxZD^2L(cghKc(LvN9VeA2D&ATP"
            ],
            "timestamp_iso8601": "2025-11-11T22:05:54",
            "hmac": "df20ca1c52f8942a9f0060ab28cba8fe39dff942dd29fc1dec093c46ef3bfd78"
        }
    ],
    "final_signature": "ee2c5a6dfde4c38db97857ba82487ecac6c0f575cebeaf9aabd80ba338aff149",
    "timestamp_iso8601": "2025-11-11T22:05:54",
    "hmac": "3860703290991125b02db66efee85f4a76e2bb0ef7ecb4fe9451428056936f61"
}

"""