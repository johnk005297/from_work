#
#
version = '1.5'

import requests
import json
import os
import xml.etree.ElementTree as ET
import sys
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)
import logging
import shutil



'''     GLOBAL VARIABLES    '''
pwd = os.getcwd()
possible_request_errors: tuple = (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, 
                                      requests.exceptions.HTTPError, requests.exceptions.InvalidHeader, requests.exceptions.InvalidURL,)

''''''''''''''''''''''''''''''

#------------------------------------------------------------------------------------------------------------------------------#


def get_server_url_and_token():

    server_url: str = input("Enter server URL: ").lower().strip()
    server_url = server_url[:-1] if server_url[-1:]=='/' else server_url
    

    headers = {'accept': '*/*', 'Content-type':'application/json; charset=utf-8'}

    ''' block to check both ports: 80 and 443 ''' # Added fix if url is set with redirect to another source
    for x in range(2):
        try:            
            check_url_request = requests.get(url=server_url+'/api/Providers', headers=headers, verify=False, allow_redirects=False, timeout=2)
            if check_url_request.status_code == 200:
                break
            elif check_url_request.status_code in (301, 302):   # This part needs to fix issues if the redirect had been set up.
                server_url = server_url[:4] + server_url[5:] if server_url[4] == 's' else server_url[:4] + 's' + server_url[4:]

        except possible_request_errors as err:
            logging.error(f"Connection error via '{server_url[:server_url.index(':')]}':\n{err}.")
            server_url = server_url[:4] + server_url[5:] if server_url[4] == 's' else server_url[:4] + 's' + server_url[4:]
            if x == 1:
                logging.error(f"Check host connection to {server_url}.")
            continue

    response = check_url_request.json()
    list_of_providersID: list = [dct['id'] for dct in response]

    url_auth = f'{server_url}/api/Auth/Login'
    confirm_username = input("Enter login(default, admin): ")
    confirm_password = input("Enter password(default, Qwerty12345!): ")
    username=confirm_username if confirm_username else 'admin'
    password=confirm_password if confirm_password else 'Qwerty12345!'

    for id in list_of_providersID:
        payload = {
                    "username": username,
                    "password": password,
                    "providerId": id
                }
        data = json.dumps(payload)
    
        auth_request = requests.post(url_auth, data=data, headers=headers, verify=False)
        response = auth_request.json()

        '''  
        Block is for checking authorization request. 
        Correct response of /api/Auth/Login method suppose to return a .json with 'access_token' and 'refresh_token'. 
        '''
        if auth_request.status_code  in (200, 201, 204):
            token = response['access_token']
            break
        elif auth_request.status_code == 401:
            def logging_error():
                print(f"--- {message} ---",'\n')
                logging.error(f"{message}")
                logging.error(f"ProviderID: {id}, response: {auth_request.status_code} [{username}/{password}]\n{auth_request.text}")
                if sys.platform == 'win32':
                    os.system('pause')
                sys.exit()
            if response.get('type') and response.get('type') == 'TransitPasswordExpiredBimException':
                message = f"Password for [{username}] has been expired!"
                logging_error()
            elif response.get('type') and response.get('type') == 'IpAddressLoginAttemptsExceededBimException':
                message = "Too many authorization attempts. IP address has been blocked!"
                logging_error()
            elif response.get('type') and response.get('type') == 'AuthCommonBimException':
                message = f"Unauthorized access. Check credentials: {username}/{password}"
                logging_error()
        else:
            logging.error(f"ProviderID: {id}, response: {auth_request.status_code} [{username}/{password}]\n{auth_request.text}")

    return server_url, token


def get_server_url_and_headers():
    server_url, token = get_server_url_and_token()
    headers = {'accept': '*/*', 'Content-type':'application/json', 'Authorization': f"Bearer {token}"}
    return server_url, headers


def create_folder_for_files_and_logs_export():

    # if 'files' folder from previous export procedure exists, it will be deleted to create a new one.
    if os.path.isdir('files'):
        shutil.rmtree('files')
    else: pass

    os.mkdir('files')
    os.mkdir(f'{pwd}/files/logs')    

    if os.path.isdir(f"{pwd}/files") == False:     
        print("Folder 'files' wasn't created. Exit.")
        sys.exit()
    elif os.path.isdir(f"{pwd}/files/logs") == False:
        print("Folder 'logs' wasn't created. Exit.")
        sys.exit()
    else:
        pass

    logging.basicConfig(filename=f"{pwd}/files/logs/export_log.txt", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s - %(message)s", filemode="w", datefmt='%d-%b-%y %H:%M:%S')


def create_folder_for_files_and_logs_import():
    if os.path.isdir(f"{pwd}/files") == False:
        logging.error("Folder 'files' is missing.")
        sys.exit("Folder 'files' is missing. Exit.")
    elif os.path.isdir(f"{pwd}/files/logs") == False:
        os.mkdir(f"{pwd}/files/logs")
    else:
        pass

    logging.basicConfig(filename=f"{pwd}/files/logs/import_log.txt", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s - %(message)s", filemode="w", datefmt='%d-%b-%y %H:%M:%S')


def define_workFlow_node_export():
    
    '''   Function creates a file 'workflow_nodes.txt' with chosen workflow nodes in it.   '''

    with open(f"{pwd}/files/workflow_nodes.txt", mode='w',encoding='utf-8'): pass

    # Check if the 'workflow_nodes.txt' was created
    if os.path.isfile(f"{pwd}/files/workflow_nodes.txt"):
        pass
    else:
        logging.error("File 'workflow_nodes.txt' hasn't been created. Exit.")
        sys.exit("File 'workflow_nodes.txt' hasn't been created. Exit.")

    workflow_node_selected: list = input("Chose nodes to export workflows from. Use whitespaces in-between. \nDraft(1) || Archived(2) || Active(3)\n\nType 'q' for exit: ").lower().split()

    if 'q' in workflow_node_selected:
        sys.exit("\nStop export process!")

    if '1' in workflow_node_selected or 'draft' in workflow_node_selected:
        with open(f"{pwd}/files/workflow_nodes.txt", 'a', encoding='utf-8') as file:
            file.write("Draft_workflows_export_server.json\n")

    if '2' in workflow_node_selected or 'archived' in workflow_node_selected:
        with open(f"{pwd}/files/workflow_nodes.txt", 'a', encoding='utf-8') as file:
            file.write("Archived_workflows_export_server.json\n")

    if '3' in workflow_node_selected or 'active' in workflow_node_selected:
        with open(f"{pwd}/files/workflow_nodes.txt", 'a', encoding='utf-8') as file:
            file.write("Active_workflows_export_server.json\n")


def read_from_json(path_to_file,file_name):
    ''' Read from JSON files, and provide dict in return. Need to pass two arguments in str format: path and file name. '''

    file_name + '.json' if file_name[-5:] != '.json' else file_name

    with open(f'{path_to_file}/{file_name}', 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)

    return data_from_json


def get_workflow_nodes_export():
    ''' Getting Draft, Archived and Active nodes Id.  '''

    url = server_url + "/api/WorkFlowNodes"
    try:
        request = requests.get(url, headers=headers_export, verify=False)
        response = request.json()
    except possible_request_errors as err:
        logging.error(f"{err}\n{request.text}") 
        sys.exit(f"Error: Couldn't export workFlow nodes. Exit.\n\n{err}")

    with open(f'{pwd}/files/workflow_nodes_export_server.json', 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

    print("  - Get workflow nodes:                          done")
    
#------------------------------------------------------------------------------------------------------------------------------#


def get_object_model_export():    
    ''' 
        Function gets model object from export server, and writes it in model_object_export_server.json file.
        /api/Integration/ObjectModel/Export  - api service
    '''

    url = server_url + "/api/Integration/ObjectModel/Export"
    try:
        request = requests.get(url, headers=headers_export, verify=False)
        response = request.json()
    except possible_request_errors as err:
        logging.error(f"{err}\n{request.text}")
        sys.exit(f"Error: Couldn't export object model. Exit.\n\n{err}")

    with open(f"{pwd}/files/model_object_export_server.json", "w", encoding="utf-8") as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)


    print("  - Get object model:                            done")
    logging.info(f"Object model has been exported. 'model_object_export_server.json' file is ready.")    

#------------------------------------------------------------------------------------------------------------------------------#


def get_workflows_export():
    ''' Get all workFlows from the chosen node. '''

    data = read_from_json(f"{pwd}/files", "workflow_nodes_export_server.json")
    for obj in range(len(data)):
        key = data[obj]['name']
        value = data[obj]['id']
        
        url = f"{server_url}/api/WorkFlowNodes/{value}/children"
        try:
            request = requests.get(url, headers=headers_export, verify=False)
            response = request.json()
        except possible_request_errors as err:
            logging.error(f"{err}\n{request.text}")

        with open(f"{pwd}/files/{key}_workflows_export_server.json", 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)
    
    logging.info(f"'{key}_workflows_export_server.json' file is ready.")


#------------------------------------------------------------------------------------------------------------------------------#


def get_workflow_xml_export():
    ''' XML for every workflow will be exported from the 'workFlow_nodes.txt' file. '''
    
    with open(f"{pwd}/files/workflow_nodes.txt", 'r', encoding='utf-8') as file:
        workflow_nodes: list = [line[:-1] for line in file]     # append all workflow nodes from the workflow_nodes.txt
                                                                # line[:-1] removes the last symbol, because 'workflow_nodes.txt' always has '\n' - newline, as a last symbol
    
    for node in workflow_nodes:
        workFlow_data = read_from_json(f"{pwd}/files", node)

        for line in workFlow_data['workFlows']:
            url = f"{server_url}/api/Attachments/{line['attachmentId']}"
            request = requests.get(url, headers=headers_export, verify=False)  

            with open(f"{pwd}/files/{line['originalId']}.xml", 'wb') as file:
                file.write(request.content)


#------------------------------------------------------------------------------------------------------------------------------


def get_workFlowId_and_bimClassId_from_export_server():   # /api/WorkFlows/{workFlowOriginId}/BimClasses
    '''
        This function does mapping between workFlow_id and bimClass_id. 
        It uses list comprehension block for transformation list of objects into dictionary with {'workFlow_id': 'bimClass_id'} pairs.
    '''

    workFlow_id_bimClass_id_export: list = []  # temp list to store data

    if os.path.isfile(f"{pwd}/files/workflow_nodes.txt"):
        with open(f"{pwd}/files/workflow_nodes.txt", 'r', encoding='utf-8') as file:
            workflow_nodes: list = [line[:-1] for line in file]     # append all workflow nodes from the workflow_nodes.txt
                                                                    # line[:-1] removes the last symbol, because 'workflow_nodes.txt' always has '\n' - newline, as a last symbol
    else:
        logging.error("No 'workflow_nodes.txt' file. Check files folder.")
        sys.exit("No workflow_nodes.txt file. Check files folder. Exit.")

    print(f"  - Get workflows:")
    for node in workflow_nodes:
        workFlow_data = read_from_json(f"{pwd}/files", node)
        for line in workFlow_data['workFlows']:
                print(f"     {line['name']}")   # display the name of the process in the output
                url = f"{server_url}/api/WorkFlows/{line['originalId']}/BimClasses"
                request = requests.get(url, headers=headers_export, verify=False)
                response = request.json()
                
                with open(f"{pwd}/files/{line['id']}.json", 'w', encoding='utf-8') as file:
                    json.dump(response, file, ensure_ascii=False, indent=4)

                # write list with active workFlows BimClasses ID in format [workFlow_id, bimClass_id]
                workFlow_id_bimClass_id_export.append(line['originalId'])
                workFlow_id_bimClass_id_export.append(response[0]['id'])
        

    # List comprehension block for transformation list of values into {'workFlow_id': 'bimClass_id'} pairs.
    tmp = workFlow_id_bimClass_id_export
    tmp: list = [ [tmp[x-1]] + [tmp[x]] for x in range(1, len(tmp), 2) ]      # generation list in format [ ['a', 'b'], ['c', 'd'], ['e', 'f'] ]
    workFlow_id_bimClass_id_export = dict(tmp)                                # transform tmp list from above to dictionary using dict() function in format {"workFlow_id": "bimClass_id"}
        

    with open(f"{pwd}/files/workFlow_id_bimClass_id_export.json", 'w', encoding='utf-8') as file:
        json.dump(workFlow_id_bimClass_id_export, file, ensure_ascii=False, indent=4)
    
    logging.info("Mapping between workflow_ID and bimClass_ID: done. 'workFlow_id_bimClass_id_export.json' file is ready.")
    print("  - Mapping between workflow_ID and bimClass_ID: done")
#------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#


def define_procedure():
    answer = input("Export(1) || Import(2): ").lower()
    if answer not in ('1', '2', 'export', 'import'):
        logging.info("No choice was made on procedure [export or import].")
        sys.exit("Nothing was chosen. Exit.")
    return True if answer in ('1', 'export') else False


def ask_about_process():
    answer = input("Need to export processes? (Y/N): ").lower()
    if answer not in ('y','n'):
        logging.info("No choice was made on processes.")
        sys.exit("Nothing was chosen. Exit.")
    return True if answer == 'y' else False


def ask_about_object_model():
    answer = input("Need to export object model? (Y/N): ").lower()
    if answer not in ('y','n'):
        logging.info("No choice was made on object model.")
        sys.exit("Nothing was chosen. Exit.")
    return True if answer == 'y' else False


def mark_begin():
    print("\n================== BEGIN export procedure ==================\n")


def mark_finish():
    print("\n================== END export procedure ====================\n")
    if sys.platform == 'win32':
        os.system('pause')


if __name__ == "__main__":
    print(f'v{version}')
    purpose = define_procedure()
    if purpose: # if export
        create_folder_for_files_and_logs_export()
        server_url, headers_export = get_server_url_and_headers()
        mark_begin()
        if ask_about_object_model():
            get_object_model_export()
        if ask_about_process():
            workflow_node = define_workFlow_node_export()
            get_workflow_nodes_export()
            get_workflows_export()
            get_workflow_xml_export()
            get_workFlowId_and_bimClassId_from_export_server()
        mark_finish()
    else:   # if import
        import import_data
