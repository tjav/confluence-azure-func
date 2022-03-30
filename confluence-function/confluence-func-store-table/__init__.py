# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
import yaml
from azure.identity import AzureCliCredential
from azure.storage.blob import ContainerClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
import uuid
# import json

# import azure.functions as func

# def main(req: func.HttpRequest, message: func.Out[str], input: list, unit: str) -> func.HttpResponse:

#     rowKey = str(uuid.uuid4())

#     data = {
#         "OARID": str(unit),
#         "Services": str(input),
#         "PartitionKey": "message",
#         "RowKey": rowKey
#     }

#     message.set(json.dumps(data))

#     return func.HttpResponse(f"Message created with the rowKey: {rowKey}")

def upload(files,unit):
    #container_client = ContainerClient.from_connection_string(connection_string, container_name)
    table_service = TableServiceClient.from_connection_string(conn_str=os.environ['tableConnection'])
    print("Uploading to table...")
    
    for file in files:        
        table_client = table_service.get_table_client("functionconf")  
        rowKey = str(uuid.uuid4())
        entity = {
        "PartitionKey": "services",
        "RowKey": rowKey,
        "OARID": str(unit),
        "Service": str(file)        
        }
        table_client.create_entity(entity=entity)
        print(f'{file} uploaded to blob storage')
    
    return (f'{unit} uploaded to blob storage')
        

def main(input: list) -> str:
    
    result = upload(input[0],input[1])
    return result
