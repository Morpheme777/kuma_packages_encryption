import sys
import os
import argparse
import json

# pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# pip install pymongo
# ?pip install bson
import bson
import codecs

class EncoderForBytesObj(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("utf-8") # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def decrypt(input_file, output_file, key, pretty):
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    
    decrypted_data = aes_decrypt(ciphertext, key)
    json_data = decode_bson(decrypted_data)

    with open(output_file, 'w', encoding='utf8') as f:
        indent = 2 if pretty else None
        json.dump(json_data, f, cls = EncoderForBytesObj, indent = indent)

def encrypt(input_file, output_file, key):
    with codecs.open(input_file, 'r') as f:
        json_data = json.load(f)

    bson_data = encode_bson(json_data)
    encrypted_data = aes_encrypt(bson_data, key)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def aes_decrypt(ciphertext, key):
    nonce, authtag = ciphertext[:12], ciphertext[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext[12:-16], authtag)
    except Exception as e:
        exit(f'Error while decrypt: {str(e)}\nCheck your password')
    return data

def aes_encrypt(text, key):
    cipher = AES.new(key, AES.MODE_GCM, nonce=os.urandom(12))
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text)
    return nonce + ciphertext + tag

def password_to_key(password):
    h = SHA256.new()
    h.update(password.encode())
    return h.digest()

def decode_bson(data):
    decoded_data = bson.BSON(data).decode()
    return decoded_data

def encode_bson(data):
    encoded_data = bson.BSON.encode(data)
    return encoded_data

### Start program ###
parser = argparse.ArgumentParser(f'python3 {sys.argv[0]}')
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", action = 'store_true', help = 'decrypt package', required=False)
group.add_argument("-e", action = 'store_true', help = 'encrypt package', required=False)
parser.add_argument("-p", metavar = 'PASSWORD', help = 'password', required=True)
parser.add_argument("-f", metavar = 'FILE', help = 'input file', required=True)
parser.add_argument("-o", metavar = 'FILE', help = 'output file', required=True)
parser.add_argument("--pretty", action = 'store_true', help = 'human readable format with indents', required=False)
args = parser.parse_args()
if args.d == args.e:
    parser.print_help()
    exit('Error: choose an action encrypt (-e) or dycrypt (-d)')

password = args.p
input_file = args.f
output_file = args.o
pretty = args.pretty
key = password_to_key(password)

if args.d:
    decrypt(input_file, output_file, key, pretty)
elif args.e:
    encrypt(input_file, output_file, key)
