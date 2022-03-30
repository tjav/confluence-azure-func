import os
import yaml
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity

def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

config = load_config()

table_service = TableServiceClient.from_connection_string(conn_str=config["azure_storage_connectionstring"])

table_name = "confluenceresources"

'''
list_tables = table_service.list_tables()
print("Listing tables:")
for table in list_tables:
    print("\t{}".format(table.name))
'''
table_client = table_service.get_table_client("confluenceresources")
entities = list(table_client.list_entities())
pdConfluence = pd.DataFrame(data = list(table_client.list_entities()))
#print(pdConfluence)

table_client = table_service.get_table_client("azureresources")
entities = list(table_client.list_entities())
pdAzure = pd.DataFrame(data = list(table_client.list_entities()))
#print(pdAzure)

outer_join_df=pd.merge(pdConfluence, pdAzure, on=['OARID','Service'], how='outer')

list_of_lists = outer_join_df.values.tolist()  

table_service = TableServiceClient.from_connection_string(conn_str=config["azure_storage_connectionstring"])
table_service.create_table_if_not_exists("joinresources")
#res = setTable("joinresources", list_of_lists, table_service.get_table_client("joinresources"))

table_client = table_service.get_table_client("joinresources")  

i=0
for el in list_of_lists:
    azure=0
    confluence=0
    if(str(el[0])!="nan"):
        #print(str(el[0]))
        azure=1
    if(str(el[4])!="nan"):
        confluence=1
    entity = {
        "PartitionKey": str(i),
        "RowKey": str(i),
        "Service": str(el[2]),
        "OARID": str(el[3]),
        "Azure": str(azure),
        "Confluence": str(confluence)
    }
    table_client.create_entity(entity=entity)
    i = i+1
