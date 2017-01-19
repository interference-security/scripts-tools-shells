# Source: https://gist.github.com/metall0id/bb3e9bab2b7caee90cb7
# Author : Tyrone Erasmus
# Version : 1.0
# Description: Decode WebSphere passwords that use {xor} prepended tag
#

#!/usr/bin/python

import argparse
import base64
import sys

# Decoded password
password = ""

# Read arguments
parser = argparse.ArgumentParser(description='Decode WebSphere passwords that use {xor} prepended tag.')
parser.add_argument('encoded_password', help='The {xor} encoded password')
args = parser.parse_args()

# Remove {xor} tag if present
if args.encoded_password.startswith("{xor}"):
	args.encoded_password = args.encoded_password.replace("{xor}", "")

# Decode by base64 decoding and xor'ing with underscore
for i in base64.b64decode(args.encoded_password):
	password += chr(ord(i) ^ ord('_'))

# Output
sys.stdout.write("[+] Decoded password string = %s\n" % password)
sys.stdout.write("[+] Decoded password hex = %s\n" % "".join("\\x%s" % byte.encode("hex") for byte in password))