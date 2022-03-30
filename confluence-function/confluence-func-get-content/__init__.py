# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from atlassian import Confluence
import pandas as pd
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential


def main(name: int) -> list:
    keyvault_name = os.environ["KEYVAULT_NAME"]
    confluence_name = os.environ["CONFLUENCE_NAME"]
    KVUri = f"https://{keyvault_name}.vault.azure.net"
    
    credential = AzureCliCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    user_name= client.get_secret("username")
    pass_word= client.get_secret("password")

    print(f"{user_name} with {pass_word}")
    

    confluence = Confluence(
        url=f"https://{confluence_name}.atlassian.net",
        username=user_name.value,
        password=pass_word.value,
        cloud=True)
    page_id = name
    page_content =confluence.get_page_by_id(page_id, expand='body.storage', status=None, version=None).get('body').get('storage').get('value')
    resources = []
    table_azure_services = pd.read_html(page_content, match='Available')
    df_azure_services = table_azure_services[0]
    df = df_azure_services['Available']

    for service in df:
        resources.append(service)

    return resources

