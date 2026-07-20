import os
import glob

base_dir = "/home/aiagent/hyeongryeol_workspace/festa_global_db"
files = glob.glob(os.path.join(base_dir, "**", "*_enriched.json"), recursive=True)

for f_path in files:
    new_path = f_path.replace("_enriched.json", "_sds.json")
    os.rename(f_path, new_path)

print(f"Renamed {len(files)} files.")
