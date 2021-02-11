# _______________________________________________________________
# Update all access token rate limits on your Rollbar projects
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json, time

# _______________________________________________________________
# Initializing variables
# Place your Rollbar access tokens here
# _______________________________________________________________
account_read_token = ''
account_write_token = ''

# Time in seconds for rate limit window. Leave blank to set default
window_size = ''

# Number of occurrences allowed per window above. Leave blank to set default
window_count = ''

# _______________________________________________________________
# Get all projects associated with your Rollbar account
# _______________________________________________________________
def retrieve_projects():

    headers = {
        'X-Rollbar-Access-Token': account_read_token
    }

    payload = {}

    url = 'https://api.rollbar.com/api/1/projects'

    response = requests.request('GET', url, headers = headers, data = payload)

    # Parse the response to JSON
    response_data = response.json()

    # Getting a list of the project IDs
    rollbar_project_ids = []
    for i in response_data['result']:
        rollbar_project_ids.append(i['id'])

    return rollbar_project_ids

# _______________________________________________________________
# Get all tokens on your projects
# _______________________________________________________________
def retrieve_tokens(rollbar_projects):

    headers = {
        'X-Rollbar-Access-Token': account_read_token
    }
    
    payload = {}

    # Initialize Access Token array
    rollbar_access_tokens = []

    for i in rollbar_projects:
        url = 'https://api.rollbar.com/api/1/project/' + str(i) + '/access_tokens'

        response = requests.request('GET', url, headers = headers, data = payload)
        
        # Parse the response to JSON
        response_data = response.json()

        # Getting a list of the access tokens
        for j in response_data['result']:
            project_token_array = []
            project_token_array.append(j['project_id'])
            project_token_array.append(j['access_token'])
            rollbar_access_tokens.append(project_token_array)

    return rollbar_access_tokens

# _______________________________________________________________
# Update all tokens
# _______________________________________________________________
def update_tokens(rollbar_tokens):

    headers = {
        'X-Rollbar-Access-Token': account_write_token
    }

    payload = {
        'rate_limit_window_count': window_count,
        'rate_limit_window_size': window_size
    }

    for i in rollbar_tokens:

        url = 'https://api.rollbar.com/api/1/project/' + str(i[0]) + '/access_token/' + str(i[1])

        response = requests.request("PATCH", url, headers = headers, data = payload)

        # Parse the response to JSON
        response_data = response.json()

        # Display a success or error message
        if response_data['err'] == 0:
            print('Token: ' + str(i[1]) + ' has been updated.')
        else:
            print('Token: ' + str(i[1]) + ' has an error: ' + str(response_data['message']))



# _______________________________________________________________
# Running the functions above   
# Find a list of all your projects, then get the access tokens,
# then update them to the values set at the top
# _______________________________________________________________

# Get projects
rollbar_projects = retrieve_projects()
print('Number of projects: ' + str(len(rollbar_projects)))

# Get tokens
rollbar_tokens = retrieve_tokens(rollbar_projects)
print('Number of tokens: ' + str(len(rollbar_tokens)))

# Update tokens
update_tokens(rollbar_tokens)


