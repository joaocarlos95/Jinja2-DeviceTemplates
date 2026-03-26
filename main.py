import os
import re
import numpy as np
import pandas as pd
from classes.templater import Templater
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


EXCEL_DATA = False
ROOT_DIRECTORY = os.getenv("root_directory")


def get_excel_data(filename):

    def get_config_blocks(filename):
        df_config_blocks = pd.read_excel(filename, sheet_name='main', header=8, usecols="B:D")
        config_blocks = []
        for block in df_config_blocks.to_dict(orient='records'):
            if block['Include']:
                config_blocks.append(block['Configuration Block'])
        return config_blocks

    data_dict = {}
    config_blocks = get_config_blocks(filename)
    df = pd.read_excel(filename, sheet_name=config_blocks, header=8)
    for sheet, data in df.items():
        data = data.replace({np.nan: None})

        if sheet == 'general':
            data = data.iloc[:, 1:]
            print(data.to_dict(orient='index')[0])
            data_dict[sheet] = data.to_dict(orient='records')

        elif sheet == 'vlan':
            data = data.iloc[:, 1:]
            data_dict[sheet] = list(data.to_dict(orient='index').values())

        # else:
        #     print(f"Sheet: {sheet}")
        #     print()
        #     print(data.to_string(index=False))
        #     print()
        #     print(data.to_dict(orient='dict'))
        #     print(data.to_dict(orient='list'))
        #     print(data.to_dict(orient='series'))
        #     print(data.to_dict(orient='split'))
        #     print(data.to_dict(orient='tight'))
        #     print(data.to_dict(orient='records'))
        #     print(data.to_dict(orient='index'))
        #     print()
        #     print("--------------------------")

    print(data_dict)


def save_config(config, hostname):

    current_date = datetime.now().strftime('%Y%m%d')
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')

    path = f"{ROOT_DIRECTORY}/outputfiles/GenerateConfig/{current_date}"
    os.makedirs(f"{path}", exist_ok=True)

    filename = f"[{current_datetime}] {hostname} - jinja2_config.txt"
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)

    print(f"Saving data to file\nPath: {path}\nFilename: {filename}")
    with open(f"{path}/{filename}", mode='w', encoding='utf-8') as file:
        file.write(config)

def deep_merge(data_1, data_2):

    for key, value in data_2.items():
        if isinstance(value, dict) and key in data_1 and isinstance(data_1[key], dict):
            deep_merge(data_1[key], value)  # Recursively merge nested dictionaries
        else:
            data_1[key] = value  # Override or add new key-value pairs
    return data_1

def main():

    vendor_os = 'extreme_exos'
    hostname = 'LIS-E108-LAN-SA-XC'
    
    config_blocks = [
        'general',
        'vlan',
        'device_management',
        'port',
        'tacacs',
        'snmp',
        'cdp',
        'lldp',
        'syslog',
        'spanning_tree',
        'radius',
        'ntp',
        'dot1x'
    ]

    templater = Templater(vendor_os=vendor_os, config_blocks=config_blocks)
    j2_template = templater.get_j2_template()
    if EXCEL_DATA:
        if not os.path.exists(f"{ROOT_DIRECTORY}/inputfiles/config_data.xlsx"):
            excel_file = f"{os.getcwd()}/inputfiles/config_data.xlsx"
        else:
            excel_file = f"{ROOT_DIRECTORY}/inputfiles/config_data.xlsx"
        data = get_excel_data(filename=excel_file)
    else:
        if not os.path.exists(f"{ROOT_DIRECTORY}/inputfiles/configs/devices/{hostname}.yaml"):
            defaults_data = templater.get_j2_data_from_file(f"{os.getcwd()}/inputfiles/configs/defaults.yaml")
            device_data = templater.get_j2_data_from_file(f"{os.getcwd()}/inputfiles/configs/devices/{hostname}.yaml")
        else:
            defaults_data = templater.get_j2_data_from_file(f"{ROOT_DIRECTORY}/inputfiles/configs/defaults.yaml")
            device_data = templater.get_j2_data_from_file(f"{ROOT_DIRECTORY}/inputfiles/configs/devices/{hostname}.yaml")
        data = deep_merge(defaults_data, device_data)

    config = templater.render_config(j2_template, data, hostname=hostname)
    save_config(config, hostname)
    

if __name__ == "__main__":
    main()