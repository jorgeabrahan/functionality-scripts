import subprocess
import re


def create_output_file(wifi_list):
    lines = []
    for x in range(len(wifi_list)):
        ssid, pwd = [wifi_list[x]['ssid'], wifi_list[x]['password']]
        line = f'ssid: {ssid}\npassword: {pwd}\n'
        lines.append(line)

    with open('pwd.txt', 'w') as f:
        f.write('\n'.join(lines))


def get_wifi_keys():
    command = ['netsh', 'wlan', 'show', 'profiles']
    command_output = subprocess.run(
        command, capture_output=True).stdout.decode()
    profile_names = (re.findall(
        'All User Profile     : (.*)\r', command_output))

    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            command.append(name)
            profile_info = subprocess.run(
                command, capture_output=True).stdout.decode()
            if re.search('Security key           : Absent', profile_info):
                continue
            else:
                wifi_profile['ssid'] = name
                command.append('key=clear')
                profile_info_pass = subprocess.run(
                    command, capture_output=True).stdout.decode()
                password = re.search(
                    'Key Content            : (.*)\r', profile_info_pass)
                if password == None:
                    wifi_profile['password'] = None
                else:
                    wifi_profile['password'] = password[1]
                wifi_list.append(wifi_profile)
                command.pop()
            command.pop()

    create_output_file(wifi_list)
