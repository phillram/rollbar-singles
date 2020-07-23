####################################################################
# Delete all occurrecnces that match an RQL query
####################################################################

###################################################################
# Imports that are good to use
###################################################################
import requests
from time import sleep

###################################################################
# Your API Keys
###################################################################
project_read_token = 'token'
project_write_token = 'token'

###################################################################
# The functionality. This will create an RQL job, pull the results
# parse the occurrence IDs and then delete those ones
# Just copy and paste your working RQL query in between the triple apostrophes in the query_string
###################################################################
url = 'https://api.rollbar.com/api/1/rql/jobs/'

headers = {
    'X-Rollbar-Access-Token': project_read_token
}
payload = {
    'query_string': 
        '''
        SELECT occurrence_id
        FROM item_occurrence 
        WHERE request.url LIKE '%@%' 
        AND timestamp > unix_timestamp() - 60 * 60 * 24 * 30
        LIMIT 1000
        ''', 
        'force_refresh': '1'
    }

# Doing the API call to create an RQL job
response = requests.request('POST', url, headers=headers, data = payload)

# Parse the response to pull the RQL job ID
response_data = response.json()
rql_job_id = response_data['result']['id']
# print('RQL job ID is: ' + str(rql_job_id))


# Putting a dumb sleep right now just to fill up some time before I put good logic
sleep(120)

# Check RQL query results
url = 'https://api.rollbar.com/api/1/rql/job/' + str(rql_job_id) + ' /result?expand=job'

headers = {
    'X-Rollbar-Access-Token': project_read_token
}
payload = {}

# Send the API call and record the response
response = requests.request('GET', url, headers=headers, data = payload)
response_data = response.json()

# Check if the RQL is complete
# To be used for retry and parsing logic
rql_done = response_data['result']['job']['status']
# print('RQL job status is: ' + str(rql_done))


# Check what column the occurence ID is
occurrence_index = 0

for i in response_data['result']['result']['columns']:
    # print('RQL column ' + str(occurrence_index) + ' is: ' + str(i))

    if i == 'occurrence_id':
        occurrence_column = occurrence_index
    occurrence_index += 1

# Parse the JSON response to pull out the individual occurence_id
for i in response_data['result']['result']['rows']:
    occurrence_id = i[occurrence_column]

    # Use the occurence_id to delete occurrences via the API
    url = 'https://api.rollbar.com/api/1/instance/' + str(occurrence_id)
    headers = {
        'X-Rollbar-Access-Token': project_write_token
    }
    payload = {}

    # Do the API call and print out the occurence ID & response
    response = requests.request('DELETE', url, headers=headers, data = payload)
    print('Ocurrence: ' + str(occurrence_id) + ' --- ' + str(response.text.encode('utf8')))









