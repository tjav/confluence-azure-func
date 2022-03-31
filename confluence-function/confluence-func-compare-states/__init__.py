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
import pandas as pd
from azure.identity import AzureCliCredential
from azure.storage.blob import ContainerClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableEntity


def compare() -> str:
    table_service = TableServiceClient.from_connection_string(conn_str=os.environ['tableConnection'])

    table_name = "funcresources"


    table_client = table_service.get_table_client("functionconf")
    entities = list(table_client.list_entities())
    pdConfluence = pd.DataFrame(data=list(table_client.list_entities()))
    # print(pdConfluence)

    table_client = table_service.get_table_client("funcresources")
    entities = list(table_client.list_entities())
    pdAzure = pd.DataFrame(data=list(table_client.list_entities()))
    # print(pdAzure)

    outer_join_df = pd.merge(pdConfluence, pdAzure, on=[
                            'OARID', 'Service'], how='outer')

    list_of_lists = outer_join_df.values.tolist()


    table_service.create_table_if_not_exists("funcjoin")
    #res = setTable("joinresources", list_of_lists, table_service.get_table_client("joinresources"))

    table_client = table_service.get_table_client("funcjoin")

    i = 0
    for el in list_of_lists:
        azure = 0
        confluence = 0
        if(str(el[0]) != "nan"):
            # print(str(el[0]))
            confluence = 1
        if(str(el[4]) != "nan"):
            azure = 1
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

    return (f'Comparison Completed')

def main(input: str) -> str:
    result = compare()

    return f"{result}!"
