import os
from pathlib import Path

# BASE_DIR = project root
BASE_DIR = Path(__file__).resolve().parent

# Add project-level static dirs
static_dirs = [
    BASE_DIR / "static",  # project-level
]

# Add app-level static dirs
apps = ["blogging"]  # add other apps if needed
for app in apps:
    static_dirs.append(BASE_DIR / app / "static")

# Dictionary to store relative paths
files_seen = {}

for static_dir in static_dirs:
    if not static_dir.exists():
        continue
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(static_dir)
            if rel_path in files_seen:
                print(f"Duplicate: {rel_path} found in:")
                print(f"  - {files_seen[rel_path]}")
                print(f"  - {full_path}")
            else:
                files_seen[rel_path] = full_path
