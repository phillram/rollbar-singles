# _______________________________________________________________
# Find project access tokens with non-default rate limits on your Rollbar projects
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json

# _______________________________________________________________
# Initializing variables
# Place your Rollbar access token here
# _______________________________________________________________
account_read_token = ''

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

    # Initialize count of non-default tokens
    rollbar_nondefault_tokens = 0

    for i in rollbar_projects:
        url = 'https://api.rollbar.com/api/1/project/' + str(i) + '/access_tokens'

        response = requests.request('GET', url, headers = headers, data = payload)
        
        # Parse the response to JSON
        response_data = response.json()

        # Getting a list of the access tokens
        for j in response_data['result']:
            if j['rate_limit_window_size'] and j['rate_limit_window_count']:
                print('Project ' + str(j['project_id']) + ' has a token named "' + str(j['name']) + '" (' + str(j['access_token']) + ') with a non-default rate limit')
                rollbar_nondefault_tokens += 1

    return rollbar_nondefault_tokens

# _______________________________________________________________
# Running the functions above   
# Find a list of all your projects, then get the access tokens,
# then print out the number which have non-default rate limits
# _______________________________________________________________

# Get projects
rollbar_projects = retrieve_projects()
print('Number of projects: ' + str(len(rollbar_projects)))

# Get tokens
rollbar_tokens = retrieve_tokens(rollbar_projects)
print('Number of tokens with non-default rates: ' + str(rollbar_tokens))



