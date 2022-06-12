#
# This is linux version!

import requests
import json
import os
import xml.etree.ElementTree as ET
import sys
# from dotenv import load_dotenv    # commented when running on linux machine which can't install load_dotenv package
# load_dotenv()




token_iktest01 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkYTdmZDQ0OC1hYmVlLTQ3MTYtYjA4Mi04Yjg3NGIyY2I0MWIiLCJpc3MiOiJodHRwOi8vd2ViYXBpIiwiaWF0IjoxNjU0OTgyMTM0LCJzaWQiOiI0ZThmZTUxZi1kZTg2LTQ1MjctYjNkOC0wNGZhMTM3MWZhNmQiLCJzdWIiOiJhZG1pbiIsInVzZXJuYW1lIjoiYWRtaW4iLCJkaXNwbGF5X25hbWUiOiJTeXN0ZW0gQWRtaW5pc3RyYXRvciIsInRlbmFudF9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsInVzZXJfcm9sZSI6ImFkbWluIiwibmJmIjoxNjU0OTgyMTM0LCJleHAiOjE2NjAyNjIxMzQsImF1ZCI6Imh0dHA6Ly9mcm9udGVuZCJ9.h6FtxTUAOJmd4OwPxKXl1pwkRQSungQzCu8T2uyO164"

# token_std_p7 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjZDg5ZTZiZC0yMTI0LTQwOTAtYTJmYS1lYmQwZjViYmIwZGIiLCJpc3MiOiJodHRwOi8vd2ViYXBpIiwiaWF0IjoxNjU0NTkxMTAzLCJzaWQiOiI4YmZmNDczNS0xMDFiLTRhN2QtODU4MS05NDQxMTYzYmQ5YjciLCJzdWIiOiJhZG1pbiIsInVzZXJuYW1lIjoiYWRtaW4iLCJkaXNwbGF5X25hbWUiOiJhZG1pbiIsInRlbmFudF9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsInVzZXJfcm9sZSI6ImFkbWluIiwibmJmIjoxNjU0NTkxMTAzLCJleHAiOjE2NTk4NzExMDMsImF1ZCI6Imh0dHA6Ly9mcm9udGVuZCJ9.RKHnUGH3v_2k7bnqnoPMtGLgY23c7P_b84EqSrAu5oQ"



headers_export = {'accept': '*/*', 'Content-type':'application/json', 'Authorization': f"Bearer {token_iktest01}"}
# headers_import = {'accept': '*/*', 'Content-type':'application/json', 'Authorization': f"Bearer {token_std_p7}"}
# headers_for_xml_import = {'accept': '*/*', 'Authorization': f"Bearer {token_std_p7}"}    # specific headers without 'Content-type' for import .xml file. Otherwise request doesn't work!



'''     GLOBAL VARIABLES    '''
pwd = os.getcwd()
bimClass_id_draft_workFlows_export: dict = {}

''''''''''''''''''''''''''''''

#------------------------------------------------------------------------------------------------------------------------------#
def check_type(data):
    print(type(data))
#------------------------------------------------------------------------------------------------------------------------------#

def get_url_export():
    site_export_url: str = input("Enter export server url, like('http://address.com'): ").lower()
    return site_export_url
#------------------------------------------------------------------------------------------------------------------------------#

def create_folders():
    try:            
        os.mkdir('Archived')
        os.mkdir('Draft')
        os.mkdir('Active')

    except FileExistsError:        
        pass
    print("create_folders - \033[;38;5;34mdone\033[0;0m")        
    
#------------------------------------------------------------------------------------------------------------------------------#


def define_workFlow_node_export():
    ''' 
        Function returns a tuple of elements like ("Active", "Active_workflows_export.json") which could be accessed by index. 
        example: workflow_node[0] - "Active"
                 workflow_node[1] - "Active_workflows_export.json"                 
    '''
    
    count = 0    
    while count < 3:
        
        workflow_node_select = input("\nWhat node to export? draft(1), archived(2), active(3)\nType 'q' for exit: ").lower().capitalize()
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


# Read from JSON files, and dict in return. pwd - current working directory
# Need to pass two arguments in str format: path and file name
def read_from_json(path_to_file,file_name):
    
    if file_name[-5:] == '.json':
        pass
    else: file_name += '.json'
    with open(f'{path_to_file}/{file_name}', 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)
    
    return data_from_json

#------------------------------------------------------------------------------------------------------------------------------#


def get_workflow_nodes_export():   # Getting Draft, Archived and Active processes.    
    
    url_for_current_func = url_export + "/api/WorkFlowNodes"
    request = requests.get(url_for_current_func, headers=headers_export)
    response = request.json()
        
    with open('workflow_nodes_export_server.json', 'w') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)  
    
    print("get_workflow_nodes_export - \033[;38;5;34mdone\033[0;0m")    
    
#------------------------------------------------------------------------------------------------------------------------------#


def get_workflows_export():    

    data = read_from_json(pwd, 'workflow_nodes_export_server.json')
    for obj in range(len(data)):
        key = data[obj]['name']
        value = data[obj]['id']
        
        url = f"{url_export}/api/WorkFlowNodes/{value}/children"
        request = requests.get(url, headers=headers_export)        
        response = request.json()

        with open(f"{pwd}/{key}/{key}_workflows_export_server.json", 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)
    
    print("get_workflows_export - \033[;38;5;34mdone\033[0;0m")

#------------------------------------------------------------------------------------------------------------------------------#


def workflow_xml_export():
    
    '''  XML will be exported from the workFlow_node based on input above - [draft, archived]  
         example: workflow_node('Archived", 'Archived_workflows_export.json')  - each element in tuple can be accessed by index
    '''
    
    if workflow_node[0] == 'Draft':                
        draft_workFlows_export = read_from_json(f"{pwd}/{workflow_node[0]}", workflow_node[1])
        for line in draft_workFlows_export['workFlows']:
            url = f"{url_export}/api/Attachments/{line['attachmentId']}"
            request = requests.get(url, headers=headers_export)        
            with open(f"{pwd}/{workflow_node[0]}/{line['originalId']}.xml", 'wb') as file:
                file.write(request.content)
    
    elif workflow_node[0] == 'Archived':        
        archived_workFlows_export = read_from_json(f'{pwd}/{workflow_node[0]}', workflow_node[1])
        for line in archived_workFlows_export['workFlows']:
            url = f"{url_export}/api/Attachments/{line['attachmentId']}"
            request = requests.get(url, headers=headers_export)        
            with open(f"{pwd}/{workflow_node[0]}/{line['originalId']}.xml", 'wb') as file:
                file.write(request.content)
    
    elif workflow_node[0] == 'Active':        
        active_workFlows_export = read_from_json(f"{pwd}/{workflow_node[0]}", workflow_node[1])
        for line in active_workFlows_export['workFlows']:
            url = f"{url_export}/api/Attachments/{line['attachmentId']}"
            request = requests.get(url, headers=headers_export)        
            with open(f"{pwd}/{workflow_node[0]}/{line['originalId']}.xml", 'wb') as file:  
                file.write(request.content)


    print("workflow_xml_export - \033[;38;5;34mdone\033[0;0m")

#------------------------------------------------------------------------------------------------------------------------------


def get_workFlows_bimClass_export():   # /api/WorkFlows/{workFlowOriginId}/BimClasses
    
    workFlow_id_bimClass_id_export: list = []  # temp list to get data

    '''  XML will be exported from the workFlow_node based on input above - [Draft, Archived, Active]  
         example: workflow_node('Archived', 'Archived_workflows_export.json')  - each element in tuple can be accessed by index
    '''
    
    if workflow_node[0] == 'Draft':
        draft_workFlows_export = read_from_json(f"{pwd}/{workflow_node[0]}", workflow_node[1])
        for line in draft_workFlows_export['workFlows']:
            url = f"{url_export}/api/WorkFlows/{line['originalId']}/BimClasses"
            request = requests.get(url, headers=headers_export)
            response = request.json()            
            with open(f"{pwd}/{workflow_node[0]}/{line['id']}.json", 'w', encoding='utf-8') as file:
                json.dump(response, file, ensure_ascii=False, indent=4)

            # write dict with draft workFlows BimClasses ID in format {"workFlow_name": "bimClass_ID"}        
            workFlow_id_bimClass_id_export.append(line['originalId'])        
            workFlow_id_bimClass_id_export.append(response[0]['id'])      
    
    elif workflow_node[0] == 'Archived':
        archived_workFlows_export = read_from_json(f"{pwd}/{workflow_node[0]}", workflow_node[1])
        for line in archived_workFlows_export['workFlows']:
            url = f"{url_export}/api/WorkFlows/{line['originalId']}/BimClasses"
            request = requests.get(url, headers=headers_export)
            response = request.json()
            with open(f"{pwd}/{workflow_node[0]}/{line['id']}.json", 'w', encoding='utf-8') as file:
                json.dump(response, file, ensure_ascii=False, indent=4)
            
            # write dict with draft workFlows BimClasses ID in format {"workFlow_name": "bimClass_ID"}        
            workFlow_id_bimClass_id_export.append(line['originalId'])        
            workFlow_id_bimClass_id_export.append(response[0]['id'])

    elif workflow_node[0] == 'Active':
        active_workFlows_export = read_from_json(f"{pwd}/{workflow_node[0]}", workflow_node[1])
        for line in active_workFlows_export['workFlows']:
            url = f"{url_export}/api/WorkFlows/{line['originalId']}/BimClasses"
            request = requests.get(url, headers=headers_export)
            response = request.json()
            with open(f"{pwd}/{workflow_node[0]}/{line['id']}.json", 'w', encoding='utf-8') as file:
                json.dump(response, file, ensure_ascii=False, indent=4)   
            
            # write dict with draft workFlows BimClasses ID in format {"workFlow_name": "bimClass_ID"}
            workFlow_id_bimClass_id_export.append(line['originalId'])        
            workFlow_id_bimClass_id_export.append(response[0]['id'])


    # List comprehension block for transformation list of values into {'workFlow_id': 'bimClass_id'} pairs.
    tmp = workFlow_id_bimClass_id_export
    tmp: list = [ [tmp[x-1]] + [tmp[x]] for x in range(1, len(tmp), 2) ]      # generation list in format [ ['a', 'b'], ['c', 'd'], ['e', 'f'] ]
    workFlow_id_bimClass_id_export = dict(tmp)                          # transform tmp list from above to dictionary using dict() function in format {"workFlow_id": "bimClass_id"}
    
    with open("workFlow_id_bimClass_id_export.json", 'w', encoding='utf-8')as file:
        json.dump(workFlow_id_bimClass_id_export, file, ensure_ascii=False, indent=4)


    print("get_workFlows_bimClass_export - \033[;38;5;34mdone\033[0;0m")
    

#------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#



if __name__ == "__main__":
    url_export = get_url_export() 
    workflow_node = define_workFlow_node_export()   
    create_folders()
    get_workflow_nodes_export()
    get_workflows_export()    
    workflow_xml_export()     
    get_workFlows_bimClass_export()
    
    
    


