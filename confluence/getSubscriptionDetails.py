# Show Azure subscription information
 
import os
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.identity import AzureCliCredential
from azure.common.credentials import ServicePrincipalCredentials

tenant_id = "b36b57a2-31a9-4402-a292-6935c529ee1c"
client_id = "9103764f-32bb-4ff1-9e0c-6825d9651bc9"
client_secret = "WfG7Q~ZeJ~GSUMGVcRsYOwUuqhxE_OcbvsET2"
subscription_id = "4d3587d2-2c0b-406e-85e6-ac2e719111a4"

#credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
credential = AzureCliCredential()
print("Successfully Authenticated")
# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, subscription_id,tenant_id=tenant_id)

print("--Resource Groups--")
for item in resource_client.resource_groups.list():
    print(item.name)

print("--Resources--")
for item in resource_client.resources.list():
    print("ID: ",item.id)
    print("Location: ",item.location)
    print("Type: ",item.type)
    print("Tags: ",item.tags)
    print("===============")
