import os
import yaml
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity

# pip install pyyaml
# pip install azure-storage-blob


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)

def get_files(dir):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and not entry.name.startswith('.'):
                yield entry

def check_pres(sub, test_str):
    for ele in sub:
        if ele in test_str:
            return 0
    return 1

def upload(files, connection_string, container_name):
    #container_client = ContainerClient.from_connection_string(connection_string, container_name)
    table_service = TableServiceClient.from_connection_string(conn_str=config["azure_storage_connectionstring"])
    print("Uploading to table...")
    files = get_files(config["source_folder"]+ "/files" )
    i=0
    k=0
    names = ['AABSYS000001', 'AABSYS000002', 'AABSYS000003']
    table_service.create_table_if_not_exists("confluenceresources")
    for file in files:        
        table_client = table_service.get_table_client("confluenceresources")  
        #blob_client = container_client.get_blob_client(file.name)   
        with open(file.path, "rb") as data:
            contents =data.read()
            #blob_client.upload_blob(data)
            array = str(contents).split("'")
            array.remove('b"[')
            array.remove(']"')
            cm = ", "
            while(cm in array) :
                array.remove(cm)
            print(array)
            el = 'abc'
            for el in array:
                entity = {
                "PartitionKey": str(k),
                "RowKey": str(k),
                "Service": str(el),
                "OARID": str(names[i])
                }
                table_client.create_entity(entity=entity)
                k = k+1
            print(f'{file.name} uploaded to blob storage')
            i=i+1

config = load_config()
files1 = get_files(config["source_folder"]+ "/files" )
upload(files1, config["azure_storage_connectionstring"], config["files_container_name"])

