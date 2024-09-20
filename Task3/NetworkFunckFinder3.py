'''


Задание 3. Нахождение сетевых функций в PE-файле. Программа анализирует некий исполняемый файл и читает из него секцию импорта
и ищет там сетевые функции затем выводит инфу о наличии сетевых функций. Необходимо найти указатель на секцию импорта, найти где
имена функции расположены
Классический поиск секций импорта по смешениям и указателям


Задание 3. Нахождение сетевых функций в PE-файле.
Разработать программу, которая анализирует структуру PE-файла и находит в нем обращение к сетевым функциям. 
В результате прорамма дожна автоматически найти все файлы 
с сетевыми фикциями в указанном каталоге.
Набор обнаруживаемых сетевых функций - в файле networkFunc.txt
Поиск функций ведется в секции импорта PE файла.
 структуры PE-файла
С целью изучения можно пользоваться ресурсом
https://penet.azureedge.net/
'''


import itertools as it
import pefile
import os

# Список сетевых функций для поиска
NETWORK_FUNCTIONS = []
DIR_PATH = "C:\\Sgu-Infbez-Kate\\Task3\\PE-files"
PE_PATH = "C:\\Sgu-Infbez-Kate\\Task1\\files\\dmde-free-2.6.0.522-win32-gui\\dmde.exe"
PE_PATH2 = "C:\\Sgu-Infbez-Kate\\Task3\\npcap-1.80.exe"
PE_PATH3 = "C:\\Sgu-Infbez-Kate\\Task3\\utweb_installer.exe"


def find_network_functions(peFile):
    print(f"\n -------- Analyze {peFile} --------- \n")
    try:
        pe = pefile.PE(peFile)
    except Exception as e:
        print(f"Ошибка при открытии PE-файла: {e}")
        return

    # Ищем секцию импорта
    if not hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        print("Секция импорта не найдена.")
        return

    found_network_functions = []

    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print(f"Импортируемая библиотека: {entry.dll.decode('utf-8')}")
        
        for imp in entry.imports:
            if imp.name:
                function_name = imp.name.decode('utf-8')
                if function_name in NETWORK_FUNCTIONS:
                    found_network_functions.append(function_name)
                    print(f"Найдена сетевой функция: {function_name}")

    if not found_network_functions:
        print("Сетевые функции не найдены.")
    else:
        print(f"Обнаруженные сетевые функции: {', '.join(found_network_functions)}")

if __name__ == "__main__":
    
    with open("C:\\Sgu-Infbez-Kate\\Task3\\networkFunc.txt",'r') as f:
        contents = f.read()
        for entry in contents.split('\n'):
            NETWORK_FUNCTIONS.append(entry)

    for dirpath, dirN, fileN in os.walk(DIR_PATH):
        for file in fileN:
            file_path = os.path.join(dirpath, file)
            find_network_functions(file_path)
            
    
    # # Укажите путь к вашему PE-файлу
    # pe_file_path = 'path/to/your/file.exe'
    # find_network_functions(pe_file_path)