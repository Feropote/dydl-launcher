from pathlib import Path  # из модуля pathlib берём класс Path: "объект-путь", умеет склеивать пути, проверять и создавать папки
import json  # встроенный модуль: превращает словарь в JSON-текст (и обратно)
import minecraft_launcher_lib as mcl  # библиотека для скачивания и запуска Minecraft; "as mcl" = короткое имя (понадобится дальше)

# BASE_DIR = папка, в которой лежит ЭТОТ файл. Строим один раз вне функций,
# поэтому его видят все функции ниже (константы принято писать ЗАГЛАВНЫМИ).
# __file__           -> путь к запущенному файлу (main.py)
# Path(...)          -> превращаем строку в объект-путь
# .resolve()         -> делаем путь полным и абсолютным (не зависит от места запуска терминала)
# .parent            -> берём папку, в которой лежит файл
BASE_DIR = Path(__file__).resolve().parent


def setup_folders():  # готовит каркас лаунчера; параметров нет, потому что набор папок всегда один и тот же
    folders_to_create = ['shared', 'instances']  # список имён (кавычки = просто текст); сами папки создаются в цикле ниже

    for name in folders_to_create:  # цикл: name по очереди станет 'shared', потом 'instances'
        folder_path = BASE_DIR / name  # оператор / склеивает пути: E:\dydl_launcher + shared
        folder_path.mkdir(parents=True, exist_ok=True)  # создать папку; parents=True создаст и промежуточные, exist_ok=True не даст упасть, если папка уже есть
        print(f"Папка '{name}' создана в: {folder_path}")  # f-строка: всё в {фигурных скобках} заменяется значением переменной


def create_instance(name, mc_version):  # создаёт ОДНУ сборку; name и mc_version = "коробки", значения кладутся при вызове
    instance_dir = BASE_DIR / 'instances' / name  # папка самой сборки; 'instances' в кавычках (всегда одно и то же), name без кавычек (меняется)
    game_dir = instance_dir / '.minecraft'  # папка для игры внутри сборки (сюда игра сама положит миры, моды, настройки)
    config_path = instance_dir / 'instance.json'  # путь к файлу с данными о сборке; лежит РЯДОМ с .minecraft, а не внутри

    if instance_dir.exists():  # .exists() даёт True, если папка уже есть. Проверка стоит ДО mkdir, иначе папка существовала бы всегда
        print(f"Сборка '{name}' уже существует: {instance_dir}")  # сообщаем, что ничего создавать не будем
        return  # return = "выйти из функции прямо сейчас": всё ниже не выполнится, старый instance.json не перезапишется

    game_dir.mkdir(parents=True, exist_ok=True)  # создаём .minecraft; заодно создастся и папка сборки (parents=True)

    instance_data = {'name': name, 'mc_version': mc_version}  # словарь: подписи в кавычках слева, значения (переменные) справа
    text = json.dumps(instance_data, indent=2, ensure_ascii=False)  # словарь -> JSON-текст; indent=2 делает файл читаемым, ensure_ascii=False сохраняет русские буквы
    config_path.write_text(text, encoding='utf-8')  # записываем текст в файл; utf-8 нужен, чтобы на Windows не было кракозябр

    print(f"Сборка '{name}' создана в: {instance_dir}")  # итоговое сообщение об успехе

def show_versions():  # показывает список версий Minecraft, которые можно скачать
    versions = mcl.utils.get_version_list()
    print(f"Доступные версии Minecraft: {versions[:5]}") # показ всех версий майнкрафта с ограничением в первые 5 версий [:5] (чтобы не засорять вывод)



if __name__ == "__main__":  # выполнять только если файл запущен напрямую (а не подключён как модуль в другом файле)
    setup_folders()  # скобки пустые: в def у этой функции нет параметров
    create_instance("my_instance", "1.21.11")  # два значения: в def два параметра (name, mc_version), порядок важен
    show_versions()  # показать список версий Minecraft, которые можно скачать