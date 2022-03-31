# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import uuid
import os
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential
from azure.data.tables import TableServiceClient

def store_resources(group: str)-> str:
    TENANT_ID = os.environ['TENANT_ID']
    SUB_ID = os.environ['SUB_ID']

    credential = AzureCliCredential()
    print("Successfully Authenticated")
    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, SUB_ID,tenant_id=TENANT_ID)

    table_service = TableServiceClient.from_connection_string(conn_str=os.environ['tableConnection'])

    for item in resource_client.resources.list_by_resource_group(group):
         table_client = table_service.get_table_client("funcresources")
         rowKey = str(uuid.uuid4()) 
         if item.tags:
            print(str(item.tags))
            print("Uploading to table...")
            strtag = str(item.tags)
            array = strtag.split("'")
            array.remove('{')
            array.remove(': ')
            array.remove('}')
            if (str(array[1]).startswith( 'AABSYS' )):
                table_client = table_service.get_table_client("funcresources")  
                entity = {
                    "PartitionKey": "AzureResourceType",
                    "RowKey": str(rowKey),
                    "Name": str(item.name),
                    "Type": str(item.type),
                    "ID": str(array[1])
                    }
                table_client.create_entity(entity=entity)
                print(f'Uploaded to table storage')
    
    return (f'Success')


def main(input: str) -> str:
    result= store_resources(input)
    return f"{result}!"
