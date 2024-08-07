# kuma_packages_encryption
Tool to encrypt and decrypt the KUMA packages

# Installation
`git clone https://github.com/Morpheme777/kuma_packages_encryption`

# Requirements:
python 3.7+
- sys
- os
- argparse
- json
- Crypto

  `pip install pycryptodome`
- bson

  `pip install pymongo`

  `pip install bson  # (not sure)`

# Usage
```
usage: python3 .\kuma_package.py [-h] [-d | -e] -p PASSWORD -f FILE -o FILE [--pretty]

options:
  -h, --help   show this help message and exit
  -d           decrypt package
  -e           encrypt package
  -p PASSWORD  password
  -f FILE      input file
  -o FILE      output file
  --pretty     human readable format with indents
```

# Example
```
python .\kuma_package.py -e -p 'MyStr0ngP@ss!' -f package.json -o pacakge
python .\kuma_package.py -d -p 'MyStr0ngP@ss!' -f pacakge -o package.json --pretty
```
# Known issues
1. Problem with bson module
```
AttributeError: module 'bson' has no attribute 'BSON'
```
Solution:
```
pip uninstall bson
pip uninstall pymongo
pip install pymongo
```
