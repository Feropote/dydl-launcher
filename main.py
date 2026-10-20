from pathlib import Path
import json
BASE_DIR = Path(__file__).resolve().parent

def setup_folders():
    folders_to_create = ['shared', 'instances']

    for name in folders_to_create:
        folder_path = BASE_DIR / name
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Папка '{name}' создана в: {folder_path}")


def create_instance(name, mc_version):
    instance_path = BASE_DIR / 'instances' / name / '.minecraft'
    instance_path.mkdir(parents=True, exist_ok=True)
    print(f"Экземпляр '{name}' создан в: {instance_path}")
    instance_data = {'name': name, 'mc_version': mc_version}
    text = json.dumps(instance_data, indent=2, ensure_ascii=False)
    config_path = instance_path.parent / 'instance.json'
    config_path.write_text(text, encoding='utf-8')
    










if __name__ == "__main__":
    setup_folders()
    create_instance("my_instance", "1.21.11")