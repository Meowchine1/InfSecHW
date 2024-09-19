# Ревизор диска, взять файл разбить на 16 бит отрезки и складываете то есть посчитать хеш сумму

'''
Задание 1. Ревизор диска
Разработать программу, работающую по принципу «ревизора диска» и контролирующую целостность данных в заданном каталоге.
Программа должна уметь:
1. подсчитать ХЭШ-сумму файлов (для каждого файла отдельно) в заданном каталоге с обходом всех подкаталогов. Сохранить эти сведения для дальнейшей проверки целостности.
2. проверить целостность каталога с указанием на изменившиеся файлы.
Алгоритм подсчета ХЭШ-суммы. Файл читается как бинарный поток. Поток разбивается на 16-битные отрезки, которые складываются по XOR. Если в последнем отрезке не хватает бит до 
16, недостающее дополняется нулями.
Хэш-сумма д.б. сохранена в файле, находящемся в контролируемом каталоге, при этом сам файл не является объектом контроля.

'''
import os
import sys
from argparse import ArgumentParser
import hashlib

DIR_PATH = "C:\\Sgu-Infbez-Kate\\Task1\\files"
HASH_FILE_NAME = "hashes.txt"
HASHFILE_PATH = os.path.join(DIR_PATH, HASH_FILE_NAME) 
TEST_FILE_PATH = os.path.join(DIR_PATH,"dmde-free-2.6.0.522-win32-gui/dev9x.dll")

def calculate_hash(file):
    hash_value = 0
    bytes_count = 2
    with open(file, 'rb') as f:
        while True:
            bytes = f.read(bytes_count)
            if not bytes:  # Stop if the end of the file
                break
            mod = len(bytes) % bytes_count
            int_val = int.from_bytes(bytes, byteorder='big')
            if mod > 0:
                int_val = int_val << 8 * mod
            hash_value ^= int_val  # XOR
    return hash_value

def save_hashes():
    with open(HASHFILE_PATH, 'w') as f:
        for dirpath, dirN, fileN in os.walk(DIR_PATH):
            for file in fileN:
                file_path = os.path.join(dirpath, file)
                if file_path != HASHFILE_PATH:  # Exclude hashfile
                    file_hash = calculate_hash(file_path)
                    f.write(f"{file_path}={file_hash}\n")

def check_integrity():
    previous_hashes = {}
    previous_files = {}
    
    # Read hash file
    with open(HASHFILE_PATH, 'r') as f:
        for line in f:
            file_path, file_hash = line.strip().split('=')
            previous_hashes[file_path] = int(file_hash)
            previous_files[file_path] = 0

    new_files = []
    hash_changed = []
    deleted_files = []
    
    # Check integrity
    for dirpath, dirnames, filenames in os.walk(DIR_PATH):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if file_path != HASHFILE_PATH:  # Exclude hash file
                new_hash = calculate_hash(file_path)
                if file_path in previous_hashes:
                    previous_files[file_path] = 1
                    if previous_hashes[file_path] != new_hash:
                        hash_changed.append(file_path)
                else:
                    new_files.append(file_path)  # Новый файл
    for filename, existence  in previous_files.items():
        if not existence:
            deleted_files.append(filename)
    if len(new_files) > 0:
        print("\nNew files:", new_files)
    else:
        print("\nНовых файлов не появилось")

    if len(new_files) > 0:
        print("\nHash was changed:\n", hash_changed)
    else:
        print("\nНи один из хешей не был изменен ")
        
    if len(new_files) > 0:
        print("\nDeleted files:", deleted_files)
    else:
        print("\nНи один из файлов не был удален")
     
     


if __name__ == "__main__":
    parser = ArgumentParser(prog='DiskRevizor', description='This programm checks all catalogue s files integrity', epilog='Help')
    parser.add_argument("--catalogue", default=DIR_PATH, type=str, help="Catalogue to check")
    args = parser.parse_args()

    DIR_PATH = args.catalogue
    HASHFILE_PATH = os.path.join(DIR_PATH, HASH_FILE_NAME) 

    if os.path.exists(DIR_PATH):
        if not os.path.exists(HASHFILE_PATH):
            save_hashes()
        check_integrity()
         
    else:
        print("ERROR: Catalogue doesn't exist")   

 
