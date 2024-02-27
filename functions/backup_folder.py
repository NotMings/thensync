import subprocess
import os
from datetime import datetime


def backup_folder(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        print(f'Error: Source folder {source_folder} does not exist.')
        return

    source_folder_name = os.path.basename(
        os.path.normpath(source_folder)
    )  # 获取源文件夹的名称
    os.makedirs(destination_folder, exist_ok=True)  # 创建目标文件夹

    now = datetime.now()
    formatted_now = now.strftime('%Y%m%d_%H%M%S')
    backup_filename = f'{source_folder_name}_{formatted_now}_backup.tar.gz'
    tar_command = (
        f'tar -czf {destination_folder}/{backup_filename} -C {source_folder} .'
    )

    try:
        subprocess.run(tar_command, shell=True, check=True)
        print(f'Backup of {source_folder} completed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error during backup: {e}')
