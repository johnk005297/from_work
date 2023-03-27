#
# Tool modules to work with folders and files
import os
import platform
import logging
import json
import shutil
import time
import random
import string
import pathlib
import zipfile
from datetime import datetime


class Folder:

    def create_folder(path, folder_name):
        try:
            if not os.path.isdir(path + '/' + folder_name):
                os.mkdir(path + '/' + folder_name)
        except OSError as err:
            logging.error(err)
            return False


    def clean_folder(path_to_folder:str):
        ''' Function removes everything in provided directory. '''

        filename:str = path_to_folder.split('/')[-1]
        try:
            if os.path.isdir(path_to_folder):
                shutil.rmtree(path_to_folder, ignore_errors=True)
                time.sleep(0.10)
                os.mkdir(path_to_folder)
                time.sleep(0.10)
                print(f'\n   - {filename} folder is now empty.')
            else:
                print(f'   - no {filename} folder was found.')
        except OSError as err:
            logging.error(err)
            print("Error occured. Check the logs.")
            return False
        return True


    def get_content():
        ''' Function provides current directory content. '''

        command = "dir" if Tools.is_windows() else "ls -lha"
        return command


    def delete_folder(path_to_folder):
        try:
            shutil.rmtree(path_to_folder, ignore_errors=True)
            return True
        except:
            return False



class File:

    def read_file(path_to_file, filename):
        ''' Read from text files. In .json case function returns a dictionary. Need to pass two arguments in str format: path and file name. '''
        try:
            with open(f"{path_to_file}/{filename}", 'r', encoding='utf-8') as file:
                if os.path.splitext(f'{path_to_file}/{filename}')[1] == '.json':    # checking extension of the file
                    try:
                        content = json.load(file)
                    except json.JSONDecodeError as err:
                        print(f"Error with the {filename} file. Check the logs.")
                        logging.error(f"Error with {filename}.\n{err}")
                        return False
                    return content
                else:
                    content = file.read()
                    return content
        except OSError as err:
            logging.error(err)
            return False


    def replace_str_in_file(filepath_2read, filepath_2write, find, replace):
        '''  Function takes 4 arguments: full path for filename to read, full path for filename to write, what to find, what to put instead of what to find.  '''

        with open(filepath_2read, 'r', encoding='utf-8') as file:
            new_json = file.read().replace(find, replace)      # find/replace vars must be string
        with open(filepath_2write, 'w', encoding='utf-8') as file:
            file.write(new_json)


    def remove_file(path_to_file):
        if os.path.isfile(path_to_file):
            os.remove(path_to_file)
            return True
        return False



class Tools:

    # Function closure
    def counter(start=0):
        def start_count():
            nonlocal start
            start += 1
            return start
        return start_count


    def is_windows():
        ''' Check if OS is windows or not. '''
        return True if platform.system() == 'Windows' else False


    def create_random_name():
        ''' Create random string of 20 characters. '''

        random_name: str = ''.join(random.choice(string.ascii_letters) for x in range(20))
        return random_name


    def run_terminal_command(command=''):
        ''' Function for execution OS command in shell. '''        

        os_name = 'Windows' if Tools.is_windows() else 'Linux'
        command = input("{0} shell: ".format(os_name)).strip() if not command else command
        os.system(command)

    def connect_ssh(host='', username=''):
        ''' Establish remote ssh connection. '''

        command = f"ssh -o StrictHostKeyChecking=no {username}@{host}"
        try:
            os.system(command)
        except OSError as err:
            logging.error(err)
            return False


    def zip_files_in_dir(dirName, archName):

        directory = pathlib.Path(dirName + '/')
        with zipfile.ZipFile(archName + '.zip', mode='w') as archive:
            try:
                for file_path in directory.iterdir():
                    archive.write(file_path, arcname=file_path.name)
            except:
                print("Error occured while zipping logs.")
                return False
        return True


    def calculate_timedelta(days):
        ''' Function gets days as input data, and provides the amount of epoch seconds by subtracting provided days from current time. '''

        epoch_time:int = int(datetime.now().timestamp())
        days:int = days * 86400      # 86400 is the amount of seconds in 24 hours
        delta:int = epoch_time - days

        return delta

