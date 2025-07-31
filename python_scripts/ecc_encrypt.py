import os
import pandas as pd
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import secrets

#ECC Key Setup
private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key()

def encrypt_value(value: str, shared_key: bytes) -> str:
    """Encrypt a string using AES-GCM with a shared ECC-derived key."""
    iv = secrets.token_bytes(12)
    encryptor = Cipher(
        algorithms.AES(shared_key),
        modes.GCM(iv)
    ).encryptor()
    ciphertext = encryptor.update(value.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encryptor.tag + ciphertext).decode()

def derive_shared_key(peer_public_key):
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'encryption',
    ).derive(shared_secret)

#File Paths
base_path = "D:\\IoMT-Simulation"
output_base = "D:\\IoMT-Simulation\\encrypted_ecc"
os.makedirs(output_base, exist_ok=True)

#ECC Shared Key for Simulation
shared_key = derive_shared_key(public_key)

#Walk Through All Subfolders but Skip Output Folder
for root, _, files in os.walk(base_path):
    if output_base.lower() in root.lower():
        continue  
    for filename in files:
        if filename.endswith(".csv") and "ENV-" in filename:
            try:
                env_number = int(filename.split("ENV-")[1].split(".")[0])
            except:
                continue
            if 11 <= env_number <= 25:
                file_path = os.path.join(root, filename)
                df = pd.read_csv(file_path)

                #Encrypt Selected Fields
                for col in ["heart_rate", "bp_systolic", "bp_diastolic", "spo2", "temperature"]:
                    if col in df.columns:
                        df[col] = df[col].astype(str).apply(lambda val: encrypt_value(val, shared_key))

                output_path = os.path.join(output_base, f"encrypted_simulated_ENV-{env_number:02d}.csv")
                df.to_csv(output_path, index=False)
                print(f"✅ Encrypted and saved: {output_path}")
