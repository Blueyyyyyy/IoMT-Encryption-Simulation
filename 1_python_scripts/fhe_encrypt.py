import os
import pandas as pd
import time
import random
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding, hashes


#RSA-based FHE by:
#Applying RSA encryption with OAEP and SHA-256 (standard secure padding)
#Introducing artificial latency to reflect computational burden
#This does not implement real homomorphic operations, but simulates the
#network and encryption overhead typical of FHE in IoMT environments.

#Root Path and Output Directory
base_path = "D:/IoMT-Simulation"
output_dir = os.path.join(base_path, "encrypted_fhe")
Path(output_dir).mkdir(parents=True, exist_ok=True)

#Simulated FHE encryption using RSA with OAEP (SHA-256)
def simulate_rsa_fhe_encryption(dataframe):
    #Simulate RSA Key Generation Per Session (NOT Per Message)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    encrypted_rows = []

    for _, row in dataframe.iterrows():
        encrypted_row = {}
        for col in dataframe.columns:
            value = str(row[col]).encode()

            try:
                #RSA Encryption with OAEP and SHA-256
                encrypted = public_key.encrypt(
                    value,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                encrypted_row[col] = encrypted.hex()
            except Exception:
                encrypted_row[col] = "ENC_ERR"

        #Introduce Latency to Simulate FHE Processing Delay
        #Simulate 0.5ms–1.5ms encryption latency
        time.sleep(random.uniform(0.0005, 0.0015))  
        encrypted_rows.append(encrypted_row)

    return pd.DataFrame(encrypted_rows)

#Locate and Encrypt All CSVs for ENV-26 to ENV-40
for root, _, files in os.walk(base_path):
    for filename in files:
        if filename.endswith(".csv") and "ENV-" in filename:
            try:
                env_num = int(filename.split("ENV-")[1].split(".csv")[0])
                if 26 <= env_num <= 40:
                    full_path = os.path.join(root, filename)
                    df = pd.read_csv(full_path)

                    print(f"🔐 Simulating RSA-based FHE for ENV-{env_num}...")
                    encrypted_df = simulate_rsa_fhe_encryption(df)
                    output_file = f"rsa_fhe_encrypted_ENV-{env_num}.csv"
                    encrypted_df.to_csv(os.path.join(output_dir, output_file), index=False)
                    print(f"✅ Saved: {output_file}")
            except Exception as e:
                print(f"❌ Error with {filename}: {e}")
