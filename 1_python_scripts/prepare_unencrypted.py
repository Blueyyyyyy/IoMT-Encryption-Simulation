import os
import shutil
from pathlib import Path

#Paths
base_path = "D:/IoMT-Simulation"
output_dir = os.path.join(base_path, "unencrypted_baseline")
Path(output_dir).mkdir(parents=True, exist_ok=True)

#Loop Through Simulation Folders and Find ENV-1 to ENV-10
copied = 0
for root, _, files in os.walk(base_path):
    for filename in files:
        if filename.endswith(".csv") and "ENV-" in filename:
            try:
                env_num = int(filename.split("ENV-")[1].split(".csv")[0])
                if 1 <= env_num <= 10:
                    src_path = os.path.join(root, filename)
                    dst_path = os.path.join(output_dir, filename)
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied: {filename}")
                    copied += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

print(f"Finished. Total files copied: {copied}")
