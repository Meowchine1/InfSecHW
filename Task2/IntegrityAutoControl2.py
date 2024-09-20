
'''
Автоконтроль целостности считать хеш сумму файла, работа с pe или с elf файлы, 
исполняемый файл должен контролировать себя на целостность, программа запускается 
просчитывается свою хеш сумму и сверяет  и записывает в своё тело эту хеш сумму путём 
хитрых манипуляций перезаписи переименовании копировании. В самом исполняемом файле 
выделяется область 2байта которую при подсчете хеша не считается куда запишется хеш сумма . 
Сверка хеш суммы во второй раз запуска исполняемого файла эта утилита просто сравнивает 
изменилась ли хеш сумма или нет (сравнивает новый подсчёт с теми двумя байтами)


Проще вариант:  хранение хеш суммы в виде отдельного файла. В одном файле хранится инф первый запуск исполняемого файла  или нет


Задание 2. Автоконтроль целостности исполняемого файла
Разработать программу, контролирующую целостность своего исполнимого файла.
Хэш-сумма м.б. сохранена отдельно от контролируемого файла, но программа должна контролировать наличие этого файла и без него не работать. 
Первый запуск программы определяет "волшебное слово" в файле-хранителе хэш-суммы и по нему выясняет, 
что происходит первый запуск для определения хэш-суммы. В дальнейшем, если в файле отсутствует "волшебное слово", 
то считается, то программа должна только сверять имеющуюся там хэш-сумму с вычисленной и сообщать о результатах.
Хэш-сумма вычислется как в Задаче 1.
'''

import subprocess

import hashlib
import os
from Task1.DiskRevizor1 import calculate_hash


PE_PATH = "C:\\Sgu-Infbez-Kate\\Task2\\pe.exe"
HASH_FILE = 'C:\\Sgu-Infbez-Kate\\Task2\\hashfile.txt'

def read_hash_file():
    if not os.path.exists(HASH_FILE):
        return None
    
    with open(HASH_FILE, 'r') as f:
        lines = f.readlines()
        hash = calculate_hash(PE_PATH)
        if len(lines) == 0:
            write_hash_to_file(hash)
        else:
            if lines == hash:
                print("Целостность файла сохранена")
            else:
                print("Целостность файла нарушена")        
            
    return None

def write_hash_to_file(hash_value):
    with open(HASH_FILE, 'w') as f:
        f.write(f"{hash_value}")


def main():
    # Получаем путь к исполняемому файлу
    current_file_path = os.path.abspath(__file__)

    # Читаем хэш из файла
    stored_hash = read_hash_file()

    # Вычисляем текущий хэш
    current_hash = calculate_hash(current_file_path)

    if stored_hash is None:
        # Первый запуск, сохраняем хэш
        write_hash_to_file(current_hash)
        print("Первый запуск. Хэш сохранен.")
    else:
        # Сравниваем хэши
        if current_hash == stored_hash:
            print("Целостность файла подтверждена.")
        else:
            print("Предупреждение: целостность файла нарушена!")

def run_external_script():
    # Укажите путь к вашему внешнему скрипту
    script_path = 'C:\\Sgu-Infbez-Kate\Task2\\autocontrol.py'
    subprocess.run(['python', script_path])

if __name__ == '__main__':
     run_external_script()


 

if __name__ == "__main__":
    #main()
    # pyinstaller --onefile main.py