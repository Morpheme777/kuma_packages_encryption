# kuma_packages_encryption
Tool to encrypt and decrypt the KUMA packages

# Requirements:
- default:
sys
os
argparse
json

- pip install pycryptodome
Crypto

- pip install pymongo
bson
pip install bson

*usage*: python3 .\kuma_package.py [-h] [-d | -e] -p PASSWORD -f FILE -o FILE

*options*:
  -h, --help   show this help message and exit
  -e           encrypt package
  -p PASSWORD  password
  -f FILE      input file
  -o FILE      output file
