import subprocess
import os
import datetime


def backup_database(db_type, dump_command, db_config, db_name, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)  # 创建目标文件夹

    db_host = db_config['host']
    db_port = db_config['port']
    db_username = db_config['username']
    db_password = db_config['password']

    now = datetime.datetime.now()
    formatted_now = now.strftime('%Y%m%d_%H%M%S')
    if db_type == 'mysql':
        backup_filename = f'{db_name}_{formatted_now}_mysql_backup.sql.gz'
        db_dump_command = f'{dump_command} -h {db_host} -P {db_port} -u {db_username} -p{db_password} {db_name} | gzip > {destination_folder}/{backup_filename}'
    if db_type == 'pgsql':
        backup_filename = f'{db_name}_{formatted_now}_pgsql_backup.sql.gz'
        db_dump_command = f'{dump_command} -h {db_host} -p {db_port} -U {db_username} -d {db_name} | gzip > {destination_folder}/{backup_filename}'

    try:
        if subprocess.run(db_dump_command, shell=True, check=True).returncode == 0:
            print(f'Backup of {db_name} completed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error during backup: {e}')
