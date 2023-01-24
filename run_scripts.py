from download_from_youtube import download_from_youtube
from get_wifi_keys import get_wifi_keys
from remove_empty_folders import remove_empty_folders
from create_classes import create_classes

def run_script(option):
    match option:
        case 'a':
            download_from_youtube()
        case 'b':
            get_wifi_keys()
        case 'c':
            remove_empty_folders()
        case 'd':
            create_classes()
        case default:
            print('Selected option does NOT correspond to any script\n')
            return False
    return True

def select_script():
    print('a- download from youtube')
    print('b- get wifi keys')
    print('c- remove empty folders')
    print('d- create university folders')
    option = input('Enter the letter corresponding to the script you want to run: ').lower().rstrip()
    script_found = run_script(option)
    if (not script_found):
        select_script()

select_script()
    


