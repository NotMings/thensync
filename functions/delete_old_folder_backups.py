import subprocess
import os


def delete_old_folder_backups(destination_folder, effective_minutes):
    if not os.path.exists(destination_folder):
        print(f'Error: Folder {destination_folder} does not exist.')
        return

    find_command = f'find {destination_folder} -type f -name "*backup.tar.gz" -cmin +{effective_minutes}'

    try:
        find_command_stdout = subprocess.run(
            find_command, shell=True, check=True, stdout=subprocess.PIPE
        ).stdout.decode()
        if find_command_stdout != b'':
            for filename in find_command_stdout.split('\n'):
                if filename != '':
                    delete_command = f'rm {filename}'
                    subprocess.run(delete_command, shell=True, check=True)
                    print(f'Old backup {filename} deleted successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error during deletion: {e}')
