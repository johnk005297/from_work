#

import requests
import json
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET



load_dotenv()
token_std_h5 = os.getenv("token_std_h5")
token_study = os.getenv("token_study")


headers_export = {'accept': '*/*','Content-type':'application/json-patch+json', 'Authorization': f"Bearer {token_std_h5}"}
headers_import = {'accept': '*/*','Content-type':'application/json-patch+json', 'Authorization': f"Bearer {token_study}"}


site_export_url: str = "http://std-h5.dev.bimeister.io"
site_import_url: str = "http://study.bimeister.io"

pwd = os.getcwd()

#------------------------------------------------------------------------------------------------------------------------------#
def check_type(data):
    print(type(data))
#------------------------------------------------------------------------------------------------------------------------------#
def create_folders():
    try:
            # Create target Directory        
            os.mkdir('archived_json')
            os.mkdir('draft_json')
            os.mkdir('active_json')
            os.mkdir('archived_xml')
            os.mkdir('draft_xml')
            os.mkdir('active_xml')   
            
    except FileExistsError:        
        pass
    print("create_folders - \033[;38;5;34mdone\033[0;0m")
#------------------------------------------------------------------------------------------------------------------------------#

def read_from_json(file_name):    # Read from JSON files, and dict in return
    
    if file_name[-5:] == '.json':
        pass
    else: file_name += '.json'    
    
    with open(f'{pwd}\\{file_name}', 'r', encoding='utf-8') as file:
        data_from_json = json.load(file)
    
    return data_from_json

#------------------------------------------------------------------------------------------------------------------------------#


def get_workflow_nodes_export():   # Getting Draft, Archived and Active processes.
    
    url = site_export_url + "/api/WorkFlowNodes"
    request = requests.get(url, headers=headers_export)
    response = request.json()
        
    with open('workflow_nodes_export.json', 'w') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)  
    
    print("get_workflow_nodes_export - \033[;38;5;34mdone\033[0;0m")    
    
#------------------------------------------------------------------------------------------------------------------------------#


def get_workflows_export():    

    data = read_from_json('workflow_nodes_export.json')
    for obj in range(len(data)):
        key = data[obj]['name']
        value = data[obj]['id']

        url = f"{site_export_url}/api/WorkFlowNodes/{value}/children"
        request = requests.get(url, headers=headers_export)        
        response = request.json()

        with open(f"{key}_workflows_export.json", 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

    print("get_workflows_export - \033[;38;5;34mdone\033[0;0m")

#------------------------------------------------------------------------------------------------------------------------------#


def workflow_xml_export():    
    
    draft_workFlows_export = read_from_json("Draft_workflows_export.json")
    archived_workFlows_export = read_from_json("Archived_workflows_export.json")
    active_workFlows_export = read_from_json("Active_workflows_export.json")
    
    for line in draft_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/Attachments/{line['attachmentId']}"
        request = requests.get(url, headers=headers_export)        
        with open(f"{pwd}\\draft_xml\\{line['name']}.xml", 'wb') as file:
            file.write(request.content)
    
    for line in archived_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/Attachments/{line['attachmentId']}"
        request = requests.get(url, headers=headers_export)        
        with open(f"{pwd}\\archived_xml\\{line['name']}.xml", 'wb') as file:
            file.write(request.content)
    
    for line in active_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/Attachments/{line['attachmentId']}"
        request = requests.get(url, headers=headers_export)        
        with open(f"{pwd}\\active_xml\\{line['name']}.xml", 'wb') as file:
            file.write(request.content)


    print("workflow_xml_export - \033[;38;5;34mdone\033[0;0m")

#------------------------------------------------------------------------------------------------------------------------------


def get_workFlows_bimClass_export():   # /api/WorkFlows/{workFlowOriginId}/BimClasses
    
    # Getting data from workFlows on EXPORT server    
    draft_workFlows_export = read_from_json("Draft_workflows_export.json")      
    archived_workFlows_export = read_from_json("Archived_workflows_export.json")
    active_workFlows_export = read_from_json("Active_workflows_export.json")
        
    for line in draft_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/WorkFlows/{line['originalId']}/BimClasses"
        request = requests.get(url, headers=headers_export)
        response = request.json()
        with open(f"{pwd}\\draft_json\\{line['name']}_bimClass.json", 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
    
    for line in archived_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/WorkFlows/{line['originalId']}/BimClasses"
        request = requests.get(url, headers=headers_export)
        response = request.json()
        with open(f"{pwd}\\archived_json\\{line['name']}_bimClass.json", 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
    
    for line in active_workFlows_export['workFlows']:
        url = f"{site_export_url}/api/WorkFlows/{line['originalId']}/BimClasses"
        request = requests.get(url, headers=headers_export)
        response = request.json()
        with open(f"{pwd}\\active_json\\{line['name']}_bimClass.json", 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)   


    print("get_workFlows_bimClass_export - \033[;38;5;34mdone\033[0;0m")
    

#------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------------#



if __name__ == "__main__":
    create_folders()
    get_workflow_nodes_export()
    get_workflows_export()    
    workflow_xml_export()     
    get_workFlows_bimClass_export()
    
    

