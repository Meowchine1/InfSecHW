'''


Задание 3. Нахождение сетевых функций в PE-файле. Программа анализирует некий исполняемый файл и читает из него секцию импорта
и ищет там сетевые функции затем выводит инфу о наличии сетевых функций. Необходимо найти указатель на секцию импорта, найти где
имена функции расположены
Классический поиск секций импорта по смешениям и указателям


Задание 3. Нахождение сетевых функций в PE-файле.
Разработать программу, которая анализирует структуру PE-файла и находит в нем обращение к сетевым функциям. В результате прорамма дожна автоматически найти все файлы с сетевыми фикциями в указанном каталоге.
Набор обнаруживаемых сетевых функций - 
DeleteIPAddress
FreeMibTable
GetAdaptersAddresses
GetAnycastIpAddressEntry
GetAnycastIpAddressTable
GetBestRoute2
GetHostNameW
GetIpAddrTable
GetIpStatisticsEx
GetUnicastIpAddressTable
IcmpCloseHandle
IcmpCreateFile
IcmpCloseHandle
IcmpSendEcho
MultinetGetConnectionPerformance
MultinetGetConnectionPerformanceW
NetAlertRaise
NetAlertRaiseEx
NetApiBufferAllocate
NetApiBufferFree
NetApiBufferReallocate
NetApiBufferSize
NetFreeAadJoinInformation
NetGetAadJoinInformation
NetAddAlternateComputerName
NetCreateProvisioningPackage
NetEnumerateComputerNames
NetGetJoinableOUs
NetGetJoinInformation
NetJoinDomain
NetProvisionComputerAccount
NetRemoveAlternateComputerName
NetRenameMachineInDomain
NetRequestOfflineDomainJoin
NetRequestProvisioningPackageInstall
NetSetPrimaryComputerName
NetUnjoinDomain
NetValidateName
NetGetAnyDCName
NetGetDCName
NetGetDisplayInformationIndex
NetQueryDisplayInformation
NetGroupAdd
NetGroupAddUser
NetGroupDel
NetGroupDelUser
NetGroupEnum
NetGroupGetInfo
NetGroupGetUsers
NetGroupSetInfo
NetGroupSetUsers
NetLocalGroupAdd
NetLocalGroupAddMembers
NetLocalGroupDel
NetLocalGroupDelMembers
NetLocalGroupEnum
NetLocalGroupGetInfo
NetLocalGroupGetMembers
NetLocalGroupSetInfo
NetLocalGroupSetMembers
NetMessageBufferSend
NetMessageNameAdd
NetMessageNameDel
NetMessageNameEnum
NetMessageNameGetInfo
NetFileClose
NetFileEnum
NetFileGetInfo
NetRemoteComputerSupports
NetRemoteTOD
NetScheduleJobAdd
NetScheduleJobDel
NetScheduleJobEnum
NetScheduleJobGetInfo
GetNetScheduleAccountInformation
SetNetScheduleAccountInformation
NetServerDiskEnum
NetServerEnum
NetServerGetInfo
NetServerSetInfo
NetServerComputerNameAdd
NetServerComputerNameDel
NetServerTransportAdd
NetServerTransportAddEx
NetServerTransportDel
NetServerTransportEnum
NetWkstaTransportEnum
NetUseAdd
NetUseDel
NetUseEnum
NetUseGetInfo
NetUserAdd
NetUserChangePassword
NetUserDel
NetUserEnum
NetUserGetGroups
NetUserGetInfo
NetUserGetLocalGroups
NetUserSetGroups
NetUserSetInfo
NetUserModalsGet
NetUserModalsSet
NetValidatePasswordPolicyFree
NetValidatePasswordPolicy
NetWkstaGetInfo
NetWkstaSetInfo
NetWkstaUserEnum
NetWkstaUserGetInfo
NetWkstaUserSetInfo
NetAccessAdd
NetAccessCheck
NetAccessDel
NetAccessEnum
NetAccessGetInfo
NetAccessGetUserPerms
NetAccessSetInfo
NetAuditClear
NetAuditRead
NetAuditWrite
NetConfigGet
NetConfigGetAll
NetConfigSet
NetErrorLogClear
NetErrorLogRead
NetErrorLogWrite
NetLocalGroupAddMember
NetLocalGroupDelMember
NetServiceControl
NetServiceEnum
NetServiceGetInfo
NetServiceInstall
NetWkstaTransportAdd
NetWkstaTransportDel
NetpwNameValidate
NetapipBufferAllocate
NetpwPathType
NetApiBufferFree
NetApiBufferAllocate
NetApiBufferReallocate
WNetAddConnection2
WNetAddConnection2W
WNetAddConnection3
WNetAddConnection3W
WNetCancelConnection
WNetCancelConnectionW
WNetCancelConnection2
WNetCancelConnection2W
WNetCloseEnum
WNetCloseEnumW
WNetConnectionDialog
WNetConnectionDialogW
WNetConnectionDialog1
WNetConnectionDialog1W
WNetDisconnectDialog
WNetDisconnectDialogW
WNetDisconnectDialog1
WNetDisconnectDialog1W
WNetEnumResource
WNetEnumResourceW
WNetGetConnection
WNetGetConnectionW
WNetGetLastError
WNetGetLastErrorW
WNetGetNetworkInformation
WNetGetNetworkInformationW
WNetGetProviderName
WNetGetProviderNameW
WNetGetResourceInformation
WNetGetResourceInformationW
WNetGetResourceParent
WNetGetResourceParentW
WNetGetUniversalName
WNetGetUniversalNameW
WNetGetUser
WNetGetUserW
WNetOpenEnum
WNetOpenEnumW
WNetRestoreConnectionW
WNetUseConnection
WNetUseConnectionW
Поиск функций ведется в секции импорта PE файла.
 структуры PE-файла
С целью изучения можно пользоваться ресурсом
https://penet.azureedge.net/
'''


import itertools as it
import pefile

# Список сетевых функций для поиска
NETWORK_FUNCTIONS = [
  
]


def find_network_functions(pe_file_path):
    try:
        pe = pefile.PE(pe_file_path)
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
    
    with open(".\\networkFunc.txt",'r') as f:
        contents = f.read()
        for entry in contents.split('\n'):
            NETWORK_FUNCTIONS.append(entry) 
    print(NETWORK_FUNCTIONS)
    
    # # Укажите путь к вашему PE-файлу
    # pe_file_path = 'path/to/your/file.exe'
    # find_network_functions(pe_file_path)