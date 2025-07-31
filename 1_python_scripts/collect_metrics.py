import os
import pandas as pd
from pathlib import Path

#Base Directory
base_path = "D:/IoMT-Simulation/IoMT-Python"

#Output Summary List
summary = []

#Define Dataset Categories
folders = {
    "None": "unencrypted_baseline",
    "ECC": "encrypted_ecc",
    "RSA-FHE": "encrypted_fhe"
}

#Loop Through Each Folder and Collect Metrics
for encryption_type, folder_name in folders.items():
    folder_path = os.path.join(base_path, folder_name)

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and "ENV-" in filename:
            full_path = os.path.join(folder_path, filename)

            try:
                df = pd.read_csv(full_path)
                env_id = filename.split("ENV-")[1].split(".csv")[0]

                #Estimate Average Row Length in Bytes
                row_lengths = df.astype(str).applymap(len).sum(axis=1)
                avg_row_len = round(row_lengths.mean(), 2)

                #File Size in KB
                file_size_kb = round(os.path.getsize(full_path) / 1024, 2)

                #Simulated Encryption Time
                if encryption_type == "None":
                    sim_time = 0
                elif encryption_type == "ECC":
                    sim_time = round(len(df) * 0.001, 4)  #~1ms Per Row
                else:
                    sim_time = round(len(df) * 0.002, 4)  #~2ms Per Row

                summary.append({
                    "Environment": f"ENV-{env_id}",
                    "Encryption Type": encryption_type,
                    "File Size (KB)": file_size_kb,
                    "Avg Row Length (bytes)": avg_row_len,
                    "Simulated Encryption Time (sec)": sim_time
                })

            except Exception as e:
                print(f"⚠️ Skipped {filename}: {e}")

#Save Summary to CSV
summary_df = pd.DataFrame(summary)
output_path = os.path.join(base_path, "encryption_performance_summary.csv")
summary_df.to_csv(output_path, index=False)

print(f"\n✅ Metrics collected and saved to: {output_path}")
