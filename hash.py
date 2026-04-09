from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section
import sys
import hashlib
import os

ELF_FILE = sys.argv[1]
BIN_FILE = sys.argv[2]
HASH_OFFSET = 8      # offset nell'header
HASH_LEN = 32        # lunghezza SHA256
HEADER_SECTION = '.fw_header'  # sezione ELF header

bin_size = os.path.getsize(BIN_FILE)

print("SIZE DEL BIN " + str(bin_size))

with open(BIN_FILE, 'rb') as b:   
    sha256 = hashlib.sha256(b.read()).digest()

print("HASH : " + str(sha256.hex()))

 # ensuring files or connections close safely even if errors occur
with open(ELF_FILE, 'rb') as f:
    elf = ELFFile(f)
    section = elf.get_section_by_name('.fw_header')

    # mi dice dove cominciano i dati 
    offset = section['sh_offset']
    size = section['sh_size']

    print("Offset : " + str(offset))
    print("Size : " + str(size))
    f.seek(offset)
    raw = f.read(size)

print("RAW:", [hex(b) for b in raw])

raw = bytearray(raw)
bin_size_bytes = bin_size.to_bytes(4,'little')

for i,b in enumerate(bin_size_bytes):
    raw[i] = b

for i,b in enumerate(sha256):
    raw[i+4] = b
print(raw)

with open(ELF_FILE, 'r+b') as f:
    f.seek(offset)
    f.write(raw)

