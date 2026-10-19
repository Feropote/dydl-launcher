from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
folders_to_create = ['shared', 'instances']

for name in folders_to_create:
    folder_path =  BASE_DIR / name
    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"Папка '{name}' создана в: {folder_path}")