import itertools
import string

def xor(msg, key):
    """XOR decryption function."""
    o = ''
    for i in range(len(msg)):
        o += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return o

# Read the encrypted message from the file
with open('encrypted', 'rb') as f:
    encrypted_msg = f.read()  # Read as bytes to preserve non-printable characters

# Generate all alphanumeric keys of length 9
characters = string.ascii_letters + string.digits  # Alphanumeric characters
found_flag = False

# Brute-force through all possible combinations of keys
for key_tuple in itertools.product(characters, repeat=9):
    key = ''.join(key_tuple)
    decrypted_msg = xor(encrypted_msg.decode(errors='ignore'), key)  # Ignore decode errors

    # Check if the decrypted message contains the expected flag format
    if 'BUETCTF' in decrypted_msg:
        print(f"Possible key: {key} -> Decrypted Message: {decrypted_msg}")
        found_flag = True
        break  # Stop if we found a valid key

if not found_flag:
    print("No valid key found that contains the flag format.")
