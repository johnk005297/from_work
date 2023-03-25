#
# Script for work with license and some other small features.
import os
import sys
import time
import app_menu
import auth
import user
import license
import export_data
import import_data
from tools import Folder, File, Tools
import logs # activates with import
import mydocker
from main_local import main_local


def main():

    AppMenu_main     = app_menu.AppMenu()
    Auth_main        = auth.Auth()
    User_main        = user.User()
    License_main     = license.License()
    Export_data_main = export_data.Export_data()
    Import_data_main = import_data.Import_data()
    Docker           = mydocker.Docker()


    AppMenu_main.welcome_info_note()
    if not Auth_main.establish_connection():  # if connection was not established, do not continue
        return False

    url, token, username, password = Auth_main.url, Auth_main.token, Auth_main.username, Auth_main.password
# ---------------------------------------------------------
#   TEST ZONE
# ---------------------------------------------------------





# ---------------------------------------------------------
# http://10.168.23.161
# ---------------------------------------------------------

    while True:
        user_command = AppMenu_main.get_user_command()
        if not user_command:    # if nothing to check, loop over.
            continue

        ''' Check user privileges for everything related in the tuple below. '''
        if user_command in (
                         ['check_license']
                        ,['server_id']
                        ,['check_serverId_validation']
                        ,['apply_license']
                        ,['delete_active_license']
                        ,['activate_license']
                        ,['exp', 'wf']                   # export workFlows
                        ,['exp', 'om']                   # export object model
                        ,['list', 'wf']                  # display workFlows
                        ,['del', 'wf']                   # delete workFlows
                        ,['imp', 'wf']                   # import workFlows
                        ,['imp', 'om']                   # import object model
                        ):
            if not License_main.privileges_checked and not User_main.check_user_permissions(url, token, username, password, License_main._permissions_to_check):

                # Create/activate user
                Auth_superuser = auth.Auth(username='johnny_mnemonic', password='Qwerty12345!') # Create Auth class instance for new user
                try:
                    License_main.privileges_granted, superuser = User_main.create_or_activate_superuser(url, token, Auth_superuser.username, Auth_superuser.password)
                except TypeError:
                    continue
                # Create system role
                su_system_role_id = User_main.create_system_role(url, token)
                # Add system role to created user
                User_main.add_system_role_to_user(url, token, superuser['id'], superuser['userName'], su_system_role_id)
                # Save data about current user we are working under
                initial_user = User_main.get_current_user(url, token)
                # Add created role to current user
                Auth_superuser.providerId = Auth_main.get_local_providerId(url)  # getting provider id for created user for logon
                Auth_superuser.get_user_access_token(url, Auth_superuser.username, Auth_superuser.password, Auth_superuser.providerId) # logging in under superuser account
                # Add system role to initial user we connected
                User_main.add_system_role_to_user(url, Auth_superuser.token, initial_user['id'], username, su_system_role_id)


            ''' =============================================================================== MAIN BLOCK =============================================================================== '''
        if user_command == ['main_menu']:
            print(AppMenu_main._main_menu)
        elif user_command in (['quit'], ['connect_to_another_server']): # connect to another server isn't realized yet

            ''' Delete created user with privileges. '''
            if License_main.privileges_granted:
                User_main.remove_system_role_from_user(url, token, initial_user['id'], initial_user['userName'], su_system_role_id)
                Auth_main.get_user_access_token(url, username, password, Auth_main.providerId)
                User_main.remove_system_role_from_user(url, token, superuser['id'], superuser['userName'], su_system_role_id)
                User_main.delete_system_role(url, su_system_role_id, token)
                User_main.delete_user(url, token, superuser['id'], superuser['userName'])


            if user_command == ['quit']:
                break   # Close the menu and exit from the script.
            else:
                License_main.privileges_granted = False
                License_main.privileges_checked = False
                if not Auth_main.establish_connection():
                    return False


            ''' =============================================================================== LICENSE BLOCK =============================================================================== '''

        elif user_command == ['check_license']:
            License_main.display_licenses(url, token, username, password)
        elif user_command == ['server_id']:
            response = License_main.get_serverID(url, token)
            print("\n   - serverId:", response)
        elif user_command == ['apply_license']:
            License_main.post_license(url, token, username, password)
            # license_id:str = License_main.post_license_new(url, token, username, password)
            # License_main.put_license(url, token, license_id=license_id[0]) if license_id else print("Post license wasn't successful. Check the logs.")
        elif user_command == ['delete_active_license']:
            License_main.delete_license(url, token, username, password)
        elif user_command == ['activate_license']:
            license_id:str = input("Enter license id: ").strip()
            License_main.put_license(url, token, username, password, license_id)
        elif user_command == ['check_serverId_validation']:
            if License_main.serverId_validation(url, token, username, password):
                print("ServerId is correct.")
            else:
                print("System has licenses with different server_id. Need to report to administrator.")


            ''' =============================================================================== User objects BLOCK =============================================================================== '''

        elif user_command == ['drop', 'uo']:
            User_main.delete_user_objects(url, token)
        elif user_command == ['drop', 'uo', '-h']:
            print(User_main.delete_user_objects.__doc__)


            ''' =============================================================================== TRANSFER DATA BLOCK =============================================================================== '''

            # Export data and display/remove workFlows
        elif user_command in (['exp', 'om'], ['exp', 'wf'], ['list', 'wf'], ['del', 'wf']):
            if Export_data_main.is_first_launch_export_data:
                Folder.create_folder(os.getcwd(), Export_data_main._transfer_folder)
                time.sleep(0.1)
                Folder.create_folder(os.getcwd() + '/' + Export_data_main._transfer_folder, Export_data_main._workflows_folder)
                time.sleep(0.1)
                Folder.create_folder(os.getcwd() + '/' + Export_data_main._transfer_folder, Export_data_main._object_model_folder)
                time.sleep(0.1)
                Export_data_main.is_first_launch_export_data = False
            if user_command == ['exp', 'om']:
                Export_data_main.export_server_info(url, token)
                Export_data_main.get_object_model(Export_data_main._object_model_file, Auth_main.url, Auth_main.token)
            elif user_command == ['exp', 'wf']:
                Export_data_main.export_server_info(url, token)
                Export_data_main.export_workflows(url, token)
            elif user_command == ['list', 'wf']:
                Export_data_main.display_list_of_workflowsName_and_workflowsId(url, token)
            elif user_command == ['del', 'wf']:
                Export_data_main.delete_workflows(url, token)

            # Import data
        elif user_command == ['imp', 'wf']:
            Import_data_main.import_workflows(url, token)
        elif user_command == ['imp', 'om']:
            Import_data_main.import_object_model(url, token)

            # Clean transfer data storage
        elif user_command == ['rm', 'files']:
            Folder.clean_folder(f"{os.getcwd()}/{Export_data_main._transfer_folder}/{Export_data_main._object_model_folder}")
            Folder.clean_folder(f"{os.getcwd()}/{Export_data_main._transfer_folder}/{Export_data_main._workflows_folder}")
            File.remove_file(f"{os.getcwd()}/{Export_data_main._transfer_folder}/export_server.info")


            ''' =============================================================================== USER =============================================================================== '''

        elif user_command == ['token']:
            print(token)
        elif user_command == ['sh']:
            Tools.run_terminal_command()
        elif user_command == ['ls', '-l']:
            Tools.run_terminal_command(Folder.get_content())
        elif user_command == ['ssh', 'connect']:
            connection_data:list = input("Enter 'remote host' and 'username' separated by a space: ").strip().split()
            try:
                Tools.connect_ssh(connection_data[0], connection_data[1])
            except IndexError:
                print("Incorrect data. Can't connect.")
                continue



            ''' =============================================================================== DOCKER =============================================================================== '''

        elif isinstance(user_command, tuple) and user_command[0][0] == 'docker':
            if not Docker._check_docker:
                print("No docker found in the system.")
                continue

            if user_command[1] == 'docker help':
                print(Docker.docker_menu())
            elif user_command[1] == 'docker container ls':
                Docker.display_containers(all=False)
            elif user_command[1] == 'docker container ls -a':
                Docker.display_containers(all=True)
            elif user_command[1] == 'docker logs -i':
                container_id = user_command[0][3]
                Docker.get_container_interactive_logs(container_id)
            elif user_command[1] == 'docker logs -f':
                containers_id = [x for x in user_command[0][3:]]
                Docker.get_container_log(*containers_id, in_file=True)
            elif user_command[1] == 'docker logs -f --all':
                Docker.get_all_containers_logs()
            elif user_command[1] == 'docker logs':
                containers_id = [x for x in user_command[0][2:]]
                Docker.get_containers_logs(*containers_id)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == '--local' and len(sys.argv) == 2:
        main_local()



