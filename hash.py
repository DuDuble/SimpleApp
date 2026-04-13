from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
import sys
import hashlib
import os


ELF_FILE = sys.argv[1]
BIN_FILE = sys.argv[2]
PRIV_KEY = sys.argv[3]
HASH_OFFSET = 8      # offset nell'header
HASH_LEN = 32        # lunghezza SHA256
HEADER_SECTION = '.fw_header'  # sezione ELF header

bin_size = os.path.getsize(BIN_FILE)

with open(BIN_FILE, 'rb') as b:   
    sha256 = hashlib.sha256(b.read()).digest()

# Key Loading 

with open(PRIV_KEY,'rb') as k:
    private_key = serialization.load_pem_private_key(
        k.read(),
        password=None
    )

#print(private_key)

# RSA 
sig = private_key.sign(
    sha256,
    padding.PKCS1v15(),
    utils.Prehashed(hashes.SHA256())
)

print(sig)

 # ensuring files or connections close safely even if errors occur
with open(ELF_FILE, 'rb') as f:
    elf = ELFFile(f)
    section = elf.get_section_by_name('.fw_header')

    # mi dice dove cominciano i dati 
    offset = section['sh_offset']
    size = section['sh_size']
    f.seek(offset)
    raw = f.read(size)

raw = bytearray(raw)
bin_size_bytes = bin_size.to_bytes(4,'little')

current_index = 0

current_index = 0

for b in bin_size_bytes:
    raw[current_index] = b
    current_index += 1

for b in sha256:
    raw[current_index] = b
    current_index += 1

for b in sig:
    raw[current_index] = b
    current_index += 1

print(len(sig))


with open(ELF_FILE, 'r+b') as f:
    f.seek(offset)
    f.write(raw)

