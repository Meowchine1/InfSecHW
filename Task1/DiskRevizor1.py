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

def calculate_hash(file_path):
    hash_value = 0
    bytes_count = 2
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(bytes_count)
            if not chunk:  # If the end of the file
                break
            # If necessary, add the required number of bytes to the multiplicity
            mod = chunk % bytes_count
            if mod > 0:
                chunk += b'\x00' * (mod)
            hash_value ^= int.from_bytes(chunk, byteorder='big')  # Make XOR
    return hash_value

def save_hashes(directory, hash_file):
    with open(hash_file, 'w') as f:
        for dirpath, dirnames, filenames in os.walk(directory):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if file_path != hash_file:  # Exclude hash file
                    file_hash = calculate_hash(file_path)
                    f.write(f"{file_path},{file_hash}\n")

def check_integrity(directory, hash_file):
    current_hashes = {}
    
    # Read hash file
    with open(hash_file, 'r') as f:
        for line in f:
            file_path, file_hash = line.strip().split(',')
            current_hashes[file_path] = int(file_hash)

    changed_filenames = []
    
    # Check integrity
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if file_path != hash_file:  # Exclude hash file
                new_hash = calculate_hash(file_path)
                if file_path in current_hashes:
                    if current_hashes[file_path] != new_hash:
                        changed_filenames.append(file_path)
                else:
                    changed_filenames.append(file_path)  # Новый файл

    return changed_filenames

if __name__ == "__main__":
    directory_to_monitor = input("Введите путь к каталогу для мониторинга: ")
    hash_file_path = os.path.join(directory_to_monitor, 'hashes.txt')

    action = input("Вы хотите (1) сохранить хэши или (2) проверить целостность? (введите 1 или 2): ")

    if action == '1':
        save_hashes(directory_to_monitor, hash_file_path)
        print(f"Хэш-суммы сохранены в {hash_file_path}.")
    elif action == '2':
        changes = check_integrity(directory_to_monitor, hash_file_path)
        if changes:
            print("Изменившиеся или новые файлы:")
            for file in changes:
                print(file)
        else:
            print("Нет изменений.")
    else:
        print("Неверный ввод.")

def isFile(fpath):
    return os.path.isfile(fpath)
def isEmpty(fpath):  
    return os.path.getsize(fpath) == 0


# Args analyzing
parser = ArgumentParser(
                    prog='DiskRevizor',
                    description='This programm checks content integrity in the catalogue ',
                    epilog='Text at the bottom of help')
parser.add_argument("catalogue", type=str, help="Catalogue to check", default="")
parser.add_argument("hashfile", type=str, default="hashes.txt", help="Hash file name (it will be created if it doesn't exist)")
parser.add_argument("-h", "--hash", help="Count hash", action='store_true')
parser.add_argument("--check", help="Check integrity", action='store_true')

args = parser.parse_args()
need_hash = args.hash
need_check = args.check
catalogue = args.catalogue
hashfile = os.path.join(catalogue, args.hashfile)


if os.path.exists(catalogue):
    file = open(hashfile, 'w+')
        
    if need_hash:
        save_hashes(catalogue, hashfile)
    if need_check:
        if isEmpty(hashfile):
            save_hashes()
        check_integrity(catalogue, hashfile)
            
         
else:
    print("Catalogue doesn't exist")        
    
        

        
    


 
    
