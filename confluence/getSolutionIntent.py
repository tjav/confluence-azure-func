from atlassian import Confluence
import re

#Authentication with token from https://id.atlassian.com/manage-profile/security/api-tokens
confluence = Confluence(
    url='https://****.atlassian.net',
    username='****@****t.com',
    password='****',
    cloud=True)

#Authentication with Bearer token (longer one)
'''
confluence = Confluence(
    url='https://****.atlassian.net',
    username = '',
    password = '',
    verify_ssl = False
)
confluence.default_headers['Authorization'] = f'Bearer ****'
'''

# Provide page id
page_id = '622593'

# Get page by ID
page_content =confluence.get_page_by_id(page_id, expand='body.storage', status=None, version=None).get('body').get('storage').get('value')
body = re.sub('{group3}','', page_content, flags = re.M)
print(body)

# Get space key from content id
page_space = confluence.get_page_space(page_id)
#print(page_space)

# Get the list of labels on a piece of Content
page_labels = confluence.get_page_labels(page_id, prefix=None, start=None, limit=None)
#print(page_labels)

# Get all pages from Space
space = page_space
all_pages = confluence.get_all_pages_from_space(space, start=0, limit=100, status=None, expand=None, content_type='page')
#print(all_pages)

# Compare content and check is already updated or not
#confluence.is_page_content_is_already_updated(page_id, body)
