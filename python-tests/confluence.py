from atlassian import Confluence
import pandas as pd


confluence = Confluence(
    url='https://schaapjes.atlassian.net',
    username='tivanbee@microsoft.com',
    password="zaYjoKPwc1ebVqZQRndB0661",
    cloud=True)

page_id = 851976

page_content =confluence.get_page_by_id(page_id, expand='body.storage', status=None, version=None).get('body').get('storage').get('value')

table_azure_services = pd.read_html(page_content, match='Available')
df_azure_services = table_azure_services[0]
df = df_azure_services['Available']

for service in df:
    print(service)

print(df[0])
