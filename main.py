from pathlib import Path
import json
import minecraft_launcher_lib as mcl
import subprocess
BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR / 'shared'

def setup_folders():
    folders_to_create = ['shared', 'instances']

    for name in folders_to_create:
        folder_path = BASE_DIR / name
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Папка '{name}' создана в: {folder_path}")

def create_instance(name, mc_version):
    instance_dir = BASE_DIR / 'instances' / name
    game_dir = instance_dir / '.minecraft'
    config_path = instance_dir / 'instance.json'

    if instance_dir.exists():
        print(f"Сборка '{name}' уже существует: {instance_dir}")
        return

    game_dir.mkdir(parents=True, exist_ok=True)

    instance_data = {'name': name, 'mc_version': mc_version}
    text = json.dumps(instance_data, indent=2, ensure_ascii=False)
    config_path.write_text(text, encoding='utf-8')

    print(f"Сборка '{name}' создана в: {instance_dir}")

def show_versions():
    versions = mcl.utils.get_version_list()
    print(f"Доступные версии Minecraft: {versions[:5]}")

def install_version(mc_version):
    print(f"Скачиваем версию Minecraft {mc_version} в папку shared/versions...")
    mcl.install.install_minecraft_version(mc_version, SHARED_DIR)

def read_instance(name):
    config_path = BASE_DIR / 'instances' / name / 'instance.json'
    text = config_path.read_text(encoding='utf-8')
    data = json.loads(text)
    return data

def launch_instance(name):
    data = read_instance(name)
    game_dir = BASE_DIR / 'instances' / name / '.minecraft'

    options = mcl.utils.generate_test_options()
    options['gameDirectory'] = str(game_dir)

    command = mcl.command.get_minecraft_command(data['mc_version'],SHARED_DIR, options)
    subprocess.run(command, cwd=game_dir)

def list_instances():
    names = []
    for instance_dir in (BASE_DIR / 'instances').iterdir():
        if (instance_dir / 'instance.json').exists():
            names.append(instance_dir.name)
    return names

def choice_instance():
    names = list_instances()
    for number, name in enumerate(names, start=1):
        print(f'{number} {name}')
    choice = int(input(f'Выберите сборку : '))
    return names[choice - 1]

if __name__ == "__main__":
    setup_folders()
    # create_instance("test1.0", "1.21.11")
    launch_instance(choice_instance())
