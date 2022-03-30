import os
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.identity import AzureCliCredential
from azure.common.credentials import ServicePrincipalCredentials
import yaml
from azure.storage.blob import ContainerClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity
import json
import re

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

tenant_id = "***"
client_id = "***"
client_secret = "***"
subscription_id = "***"

# https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations
ServicesMatch = [
    ["Microsoft.Sql/servers/databases", "Azure SQL database"],
    ["Microsoft.Sql/servers", "Azure SQL Database server"],
    ["Microsoft.ManagedIdentity/userAssignedIdentities", "Managed Identity"],
    ["Microsoft.Network/applicationGateways", "Application gateway"],
    ["Microsoft.Network/privateLinkServices", "Private Link"],
    ["Microsoft.Network/virtualNetworks", "Virtual network"],
    ["Microsoft.Web/sites", "Function app"],
    ["Microsoft.Storage/storageAccounts", "Storage account"],
    ["microsoft.insights/components", "Application Insights"],
    ["Microsoft.KeyVault/vaults", "Key vault"],
    ["Microsoft.DataFactory/factories", "Azure Data Factory"]
]

#credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
credential = AzureCliCredential()
print("Successfully Authenticated")
# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, subscription_id,tenant_id=tenant_id)

config = load_config()
table_service = TableServiceClient.from_connection_string(conn_str=config["azure_storage_connectionstring"])
table_service.create_table("azureresources")

print("--Resources--")
k=0
for item in resource_client.resources.list():
    print("ID: ",item.id)
    print("Location: ",item.location)
    print("Type: ",item.type)
    print("Kind: ",item.kind)
    print("Name: ",item.name)
    print("Tags: ",item.tags)
    itemTypeName = " "
    for i in range (11):
        if item.type == ServicesMatch[i][0]:
            itemTypeName = ServicesMatch[i][1]
    print("itemTypeName: ",itemTypeName)
    print("===============")
    #x = re.search('^AABSYS', str(item.tags))
    if item.tags:
        print(str(item.tags))
        print("Uploading to table...")
        strtag = str(item.tags)
        array = strtag.split("'")
        array.remove('{')
        array.remove(': ')
        array.remove('}')
        if (str(array[1]).startswith( 'AABSYS' )):
            table_client = table_service.get_table_client("azureresources")  
            entity = {
                "PartitionKey": str(k),
                "RowKey": str(k),
                "Name": str(item.name),
                "Type": str(item.type),
                "Service": str(itemTypeName),
                "ID": str(array[1])
                }
            table_client.create_entity(entity=entity)
            k = k+1
            print(f'Uploaded to table storage')
        
