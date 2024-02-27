import os
import argparse
import yaml
from functions.backup_folder import backup_folder
from functions.delete_old_folder_backups import delete_old_folder_backups
from functions.backup_database import backup_database
from functions.delete_old_db_backups import delete_old_db_backups
from functions.storage.s3 import upload_to_s3, delete_from_s3


class Backup:
    def __init__(self, config_file):
        self.config = self.read_config_file(config_file)

    def read_config_file(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def backup_folder(self):
        for source_folder in self.config['backup']['folder']['source_folder']:
            for destination_folder in self.config['backup']['folder']['destination_folder']:
                print(f'Backing up {source_folder} to {destination_folder}')
                backup_folder(source_folder, destination_folder)

    def delete_old_folder_backups(self):
        effective_minutes = self.config['backup']['folder']['effective_minutes']
        print(f'Deleting backups older than {effective_minutes} minutes')
        for destination_folder in self.config['backup']['folder']['destination_folder']:
            delete_old_folder_backups(destination_folder, effective_minutes)

    def backup_database(self):
        mysql_config = self.config['backup']['database']['mysql']
        pgsql_config = self.config['backup']['database']['pgsql']
        if mysql_config['enabled']:
            dump_command = mysql_config['dump_command']
            for database_name in mysql_config['database']:
                database_config = mysql_config['config']
                for destination_folder in self.config['backup']['database']['destination_folder']:
                    print(f'Backing up {database_name} to {destination_folder}')
                    backup_database(
                        'mysql',
                        dump_command,
                        database_config,
                        database_name,
                        destination_folder,
                    )
        if pgsql_config['enabled']:
            dump_command = pgsql_config['dump_command']
            for database_name in pgsql_config['database']:
                database_config = pgsql_config['config']
                for destination_folder in self.config['backup']['database']['destination_folder']:
                    print(f'Backing up {database_name} to {destination_folder}')
                    backup_database(
                        'pgsql',
                        dump_command,
                        database_config,
                        database_name,
                        destination_folder,
                    )

    def delete_old_db_backups(self):
        effective_minutes = self.config['backup']['database']['effective_minutes']
        print(f'Deleting backups older than {effective_minutes} minutes')
        for destination_folder in self.config['backup']['database']['destination_folder']:
            delete_old_db_backups(destination_folder, effective_minutes)

    def upload_files(self, upload_type, destination_folder):
        for storage in self.config['backup'][upload_type]['upload_to']:
            if storage == 's3':
                s3_config = self.config['storage']['s3']
                for folder in destination_folder:
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            upload_to_s3(file_path, s3_config)

    def delete_remote_files(self, upload_type, destination_folder):
        for storage in self.config['backup'][upload_type]['upload_to']:
            if storage == 's3':
                s3_config = self.config['storage']['s3']
                for folder in destination_folder:
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            delete_from_s3(file_path, s3_config)

    def run(self):
        if self.config['backup']['folder']['enabled']:
            if self.config['backup']['folder']['destination_folder'] != '':
                self.delete_remote_files('folder', self.config['backup']['folder']['destination_folder'])
                print('\n')
                self.delete_old_folder_backups()
                print('\n')
            if self.config['backup']['folder']['source_folder'] != '':
                self.backup_folder()
                print('\n')
                self.upload_files('folder', self.config['backup']['folder']['destination_folder'])
                print('\n')

        if self.config['backup']['database']['enabled']:
            if self.config['backup']['database']['destination_folder'] != '':
                self.delete_remote_files('database', self.config['backup']['database']['destination_folder'])
                print('\n')
                self.delete_old_db_backups()
                print('\n')
            if self.config['backup']['database']['mysql']['enabled'] or self.config['backup']['database']['pgsql']['enabled']:
                self.backup_database()
                print('\n')
                self.upload_files('database', self.config['backup']['database']['destination_folder'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup utility')
    parser.add_argument('--config', '-c', type=str, default='config.yaml', help='Path to the configuration file')

    args = parser.parse_args()

    backup = Backup(args.config)
    backup.run()
