#
import requests
import json
import export_data as ex      # Data from export_data.py 
import xml.etree.ElementTree as ET
import time
import sys
import os


'''     GLOBAL VARIABLES    '''
pwd = os.getcwd()

token_std_p7 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjZDg5ZTZiZC0yMTI0LTQwOTAtYTJmYS1lYmQwZjViYmIwZGIiLCJpc3MiOiJodHRwOi8vd2ViYXBpIiwiaWF0IjoxNjU0NTkxMTAzLCJzaWQiOiI4YmZmNDczNS0xMDFiLTRhN2QtODU4MS05NDQxMTYzYmQ5YjciLCJzdWIiOiJhZG1pbiIsInVzZXJuYW1lIjoiYWRtaW4iLCJkaXNwbGF5X25hbWUiOiJhZG1pbiIsInRlbmFudF9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsInVzZXJfcm9sZSI6ImFkbWluIiwibmJmIjoxNjU0NTkxMTAzLCJleHAiOjE2NTk4NzExMDMsImF1ZCI6Imh0dHA6Ly9mcm9udGVuZCJ9.RKHnUGH3v_2k7bnqnoPMtGLgY23c7P_b84EqSrAu5oQ"

headers_import = {'accept': '*/*', 'Content-type':'application/json', 'Authorization': f"Bearer {token_std_p7}"}
headers_for_xml_import = {'accept': '*/*', 'Authorization': f"Bearer {token_std_p7}"}    # specific headers without 'Content-type' for import .xml file. Otherwise request doesn't work!

''''''''''''''''''''''''''''''



def get_url_import():
    url_import: str = input("Enter import server url, like('http://address.com'): ").lower()
    return url_import
#------------------------------------------------------------------------------------------------------------------------------#


def define_workFlow_node_import():
    ''' 
        Function returns a tuple of elements like ("Active", "Active_workflows_export.json") which could be accessed by index. 
        example: workflow_node[0] - "Active"
                 workflow_node[1] - "Active_workflows_export.json"                 
    '''
    
    count = 0    
    while count < 3:
        
        workflow_node_select = input("\nWhat node to import? draft(1), archived(2), active(3)\nType 'q' for exit: ").lower().capitalize()
        if workflow_node_select == 'q':
            sys.exit("\nStop import process!")
        count += 1

        # workflow_node_select is a tuple with two values - directory and .json file
        if workflow_node_select in ('Draft', '1'):
            # workflow_node('Draft', 'Draft_workflows_export.json', 'draft')        
            return "Draft", "Draft_workflows_export_server.json"

        elif workflow_node_select in ('Archived', '2'):
            # workflow_node('Archived", 'Archived_workflows_export.json', 'archived')        
            return "Archived", "Archived_workflows_export_server.json"

        elif workflow_node_select in ('Active', '3'):
            # workflow_node('Active", 'Active_workflows_export.json', 'active'               
            return "Active", "Active_workflows_export_server.json"  

        elif count == 3:  sys.exit("\nStop import process!")          
    
#------------------------------------------------------------------------------------------------------------------------------#


def get_workflow_nodes_import():   # Getting Draft, Archived and Active processes.
    
    url_for_current_func = url_import + "/api/WorkFlowNodes"
    request = requests.get(url_for_current_func, headers=headers_import)
    response = request.json()
        
    with open('workflow_nodes_import_server.json', 'w') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)   
    print("get_workflow_nodes_import - \033[;38;5;34mdone\033[0;0m")
    
#------------------------------------------------------------------------------------------------------------------------------#

# Function needs for work on line replacement in files
def replace_str_in_file(file_in, file_out, find, replace):    
   
    with open(f"{file_in}", 'r', encoding='utf-8') as file:
        new_json = file.read().replace(find, replace)      # find, replace vars must be string
    with open(f"{file_out}", 'w', encoding='utf-8') as file:
        file.write(new_json)
        
#------------------------------------------------------------------------------------------------------------------------------#


# data takes {workFlowOriginId} as an argument
def get_BimClassID_of_current_process_import(data):  # /api/WorkFlows/{workFlowOriginId}/BimClasses
    
    url = f"{url_import}/api/WorkFlows/{data}/BimClasses"
    request = requests.get(url, headers=headers_import)
    response = request.json()    
    for object in range(len(response)):
        return response[object]['id']
    

#------------------------------------------------------------------------------------------------------------------------------#


def create_workflow_import():

    url = url_import + "/api/WorkFlows"  # POST request to create workFlow
    '''
    workflow_node tuple comes from ex.define_workFlow_node() function. It provides a selection of two components ex.("Draft", "Draft_workflows_export.json")
    which can be accessed by index.
       example:  workflow_node[0] - "Draft"
                 workflow_node[1] - "Draft_workflows_export.json"                 
    '''
    
    workflows_export_server = ex.read_from_json(f"{pwd}/{workflow_node[0]}",workflow_node[1])    
    workflow_nodes_import = ex.read_from_json(pwd,'workflow_nodes_import_server.json')     # Contains imported workflows    
    
    '''  BEGIN of POST request to create workFlows  '''
    for workflow in workflows_export_server['workFlows']:
        post_payload = {
                        "name": workflow["name"],
                        "workFlowNodeId": workflow_nodes_import[0]['id'],    # 0: Draft; 1: Archived; 2: Active;
                        "description": str(workflow["description"]),
                        "elements": [],
                        "type": workflow["type"]
                        }
        json_post_payload = json.dumps(post_payload)
        post_request = requests.post(url, data=json_post_payload, headers=headers_import)     # /api/WorkFlows/{workFlowOriginalId}
        post_response = post_request.json()
        
        bimClass_id_import = get_BimClassID_of_current_process_import(post_response['originalId'])    # reference workFlow_original_ID on import server        
        bimClass_list_id_export = ex.read_from_json(pwd, 'workFlow_id_bimClass_id_export.json')                 
        time.sleep(0.25)
        '''  END of POST request  '''
        
        '''  BEGIN OF PUT REQUEST  
            adding 'elements': [], data from workFlows export into newly created workFlow
        '''            
        put_payload = {
                        "name": workflow["name"],
                        "workFlowNodeId": workflow_nodes_import[0]['id'],    # 0: Draft; 1: Archived; 2: Active;
                        "description": str(workflow["description"]),
                        "elements": workflow['elements'],
                        "type": workflow["type"]
                        }
        json_put_payload = json.dumps(put_payload)
        
        # Replacement of workFlow_bimClass_ID from export server with bimClass_ID newly created workFlow on import server
        changed_put_payload = json_put_payload.replace(bimClass_list_id_export[workflow["originalId"]], bimClass_id_import)
        requests.put(url+"/"+post_response['originalId'], data=changed_put_payload, headers=headers_import)   # /api/WorkFlows/{workFlowOriginalId}  
        time.sleep(0.25)
        '''  END OF PUT REQUEST  '''
        

        '''  BEGIN OF XML POST REQUEST  '''      
        xml_path = pwd + "/" + workflow_node[0]

        payload={}
        files=[ ('file',(f'{workflow["originalId"]}.xml',open(f'{xml_path}/{workflow["originalId"]}.xml','rb'),'text/xml'))  ]
                        
        post_xml_request = requests.post(f"{url}/{post_response['originalId']}/Diagram?contentType=file", headers=headers_for_xml_import, data=payload, files=files)
        # print(f"{post_xml_request.status_code}")
        print(f"Name of process: {post_response['name']}",end=' ')
        print(f"\033[;38;5;34m{post_xml_request.status_code}\033[0;0m" if post_xml_request.status_code == 200 else f"\033[;38;5;9m{post_xml_request.status_code}\033[0;0m")
        time.sleep(0.25)
        '''  END OF XML POST REQUEST  '''
    
    print(f"create_workflow - \033[;38;5;34mdone\033[0;0m" if post_request.status_code == 201 else f"create_workflow - \033[;38;5;9m{post_request.status_code}\033[0;0m")
    
#------------------------------------------------------------------------------------------------------------------------------#



def get_workflows_import():    # Creating .json only Draft workFlows

    # workflow_nodes_import = ex.read_from_json(pwd,'workflow_nodes_import_server.json')
    data = ex.read_from_json(pwd, 'workflow_nodes_export_server.json')
    for obj in range(len(data)):
        key = data[obj]['name']
        value = data[obj]['id']
            
        url = f"{url_import}/api/WorkFlowNodes/{value}/children"
        request = requests.get(url, headers=headers_import)        
        response = request.json()

        with open(f"{pwd}/{key}/{key}_workflows_import_server.json", 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

    print("get_workflows_import - \033[;38;5;34mdone\033[0;0m")

#------------------------------------------------------------------------------------------------------------------------------#

# def delete_draft_workflows():
#     get_workflows_import()
#     data = ex.read_from_json(f"{pwd}/Draft", "Draft_workflows_import_server.json")  # Change the \

#     for obj in range(len(data)):
#         print(data[obj]['name'])
#         print(data[obj]['id'])
    # url = f"{url_import}"    # /api/WorkFlows/{workFlowOriginalId}


#------------------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":          
    url_import = get_url_import()
    workflow_node = define_workFlow_node_import()  
    get_workflow_nodes_import()
    create_workflow_import()    
    get_workflows_import()
    
