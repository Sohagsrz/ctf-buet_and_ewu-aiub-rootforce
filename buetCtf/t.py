import hashlib

def generate_valid_sha256_key():
    prefix = "3ced3f96d70eecd4409f"
    
    # Starting from a basic number to append to the prefix
    num = 0
    while True:
        # Create a candidate string by appending a number to the prefix
        candidate = prefix + format(num, 'x').zfill(64 - len(prefix))  # Fill the rest with hex digits

        # Check the length
        if len(candidate) == 64:
            # Generate the SHA-256 hash
            sha256_hash = hashlib.sha256(candidate.encode()).hexdigest()
            # Check if it starts with the desired prefix
            if sha256_hash.startswith(prefix):
                return sha256_hash
        
        # Increment the number for the next candidate
        num += 1

# Generate the license key
license_key = generate_valid_sha256_key()
print(f"Generated License Key: {license_key}")
