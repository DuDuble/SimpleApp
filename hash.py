# from elftools.elf.elffile import ELFFile
# from elftools.elf.sections import Section
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import utils
import sys
import hashlib
import os
import subprocess

ELF_FILE = sys.argv[1]
BIN_FILE = sys.argv[2]
PRIV_KEY = sys.argv[3]
ENC_KEY = sys.argv[4]

base = os.path.dirname(os.path.abspath(__file__))

imgtool = os.path.join(base, "venv/bin/imgtool")

print("imgtool path:", imgtool)
print("exists:", os.path.exists(imgtool))

subprocess.run(
    [
        imgtool,  "create",
        "--pad-header",
        "--key", PRIV_KEY,
        # "--encrypt", ENC_KEY,
        # "--encrypt-keylen", "128",
        "--align", "4",
        "--version", "1.0.0",
        "--header-size", "0x200",
        "--slot-size", "0x12000",
        BIN_FILE,
        "signed_app.bin"
    ]
)
# HASH_OFFSET = 8      # offset nell'header
# HASH_LEN = 32        # lunghezza SHA256
# HEADER_SECTION = '.fw_header'  # sezione ELF header

# bin_size = os.path.getsize(BIN_FILE)

# with open(BIN_FILE, 'rb') as b:   
#     sha256 = hashlib.sha256(b.read()).digest()

# # Key Loading 

# with open(PRIV_KEY,'rb') as k:
#     private_key = serialization.load_pem_private_key(
#         k.read(),
#         password=None
#     )

# #print(private_key)

# # RSA 
# sig = private_key.sign(
#     sha256,
#     padding.PSS(  # V2.1 Padding (PSS)
#         mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function
#         salt_length=padding.PSS.MAX_LENGTH  # Lunghezza del sale (può essere configurata)
#     ),
#     utils.Prehashed(hashes.SHA256())
# )

# print(sig)

#  # ensuring files or connections close safely even if errors occur
# with open(ELF_FILE, 'rb') as f:
#     elf = ELFFile(f)
#     section = elf.get_section_by_name('.fw_header')

#     # mi dice dove cominciano i dati 
#     offset = section['sh_offset']
#     size = section['sh_size']
#     f.seek(offset)
#     raw = f.read(size)

# raw = bytearray(raw)
# bin_size_bytes = bin_size.to_bytes(4,'little')

# current_index = 4

# for b in bin_size_bytes:
#     raw[current_index] = b
#     current_index += 1

# for b in sha256:
#     raw[current_index] = b
#     current_index += 1

# for b in sig:
#     raw[current_index] = b
#     current_index += 1

# print(len(sig))


# with open(ELF_FILE, 'r+b') as f:
#     f.seek(offset)
#     f.write(raw)

