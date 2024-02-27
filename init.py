import subprocess
import shutil
import argparse


class Init:
    def get_package_manager(self):
        package_managers = ['apt', 'yum', 'dnf', 'zypper']

        for manager in package_managers:
            if shutil.which(manager):
                return manager

        return None

    def install_package(self, package_name):
        package_manager = self.get_package_manager()
        if package_manager:
            install_command = f'{package_manager} install -y {package_name}'
            subprocess.run(install_command, shell=True, check=True)
        else:
            print('Error: No package manager found.')

    def uninstall_package(self, package_name):
        package_manager = self.get_package_manager()
        if package_manager:
            uninstall_command = f'{package_manager} remove -y {package_name}'
            subprocess.run(uninstall_command, shell=True, check=True)
        else:
            print('Error: No package manager found.')

    def run(self, action='install'):
        packages = [
            'python3-yaml',
            'python3-boto3',
        ]
        if action == 'install':
            for package in packages:
                self.install_package(package)
        else:
            for package in packages:
                self.uninstall_package(package)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup utility')
    parser.add_argument('--action', '-a', type=str, default='install', help='Action to perform (install/uninstall)')

    args = parser.parse_args()

    init = Init()
    init.run(args.action)
