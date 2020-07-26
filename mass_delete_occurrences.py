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

# Create RQL Job
#------------------------------------------
url = 'https://api.rollbar.com/api/1/rql/jobs/'

headers = {
    'X-Rollbar-Access-Token': project_read_token
}
payload = {
    'query_string': 
        '''
        SELECT *  
        FROM item_occurrence
        WHERE item.counter = 1
        ORDER BY timestamp DESC
        LIMIT 1000
        ''', 
        'force_refresh': '1'
    }

# Doing the API call to create an RQL job
response = requests.request('POST', url, headers=headers, data = payload)

# Parse the response to pull the RQL job ID
# If the RQL query is invalid, stop execution
response_data = response.json()

try:
    rql_job_id = response_data['result']['id']
    print('RQL job ID is: ' + str(rql_job_id))
except:
    print('The RQL job was not created: ' + str(response_data['message']))
    exit()


# Check RQL query results
#------------------------------------------
url = 'https://api.rollbar.com/api/1/rql/job/' + str(rql_job_id) + ' /result?expand=job'

headers = {
    'X-Rollbar-Access-Token': project_read_token
}
payload = {}

retries = 0
while True:
    # Send the API call and record the response
    response = requests.request('GET', url, headers=headers, data = payload)
    response_data = response.json()

    # Check if the RQL is complete
    rql_status = response_data['result']['job']['status']
    if str(rql_status) == 'success':
        print('RQL job completed')
        break
    # Retry three times with a 10 second pause. Quit after 3 failed attempts
    else:
        print('Status is not success. This is try: ' + str(retries))
        sleep(10)
        retries += 1
        if retries >= 3:
            print('RQL status was not success in ' + str(retries) + ' attempts. Quitting.')
            exit()


# Parse the JSON response to pull out the individual occurence_id
#------------------------------------------
# Check if there are no results from the RQL query
if not response_data['result']['result']['rows']:
    print('There are no occurrences that match your RQL query')
    exit()

# Check what column the occurence ID is
occurrence_index = 0
for i in response_data['result']['result']['columns']:
    # print('RQL column ' + str(occurrence_index) + ' is: ' + str(i))
    if i == 'occurrence_id':
        occurrence_column = occurrence_index
    occurrence_index += 1

# Pull occurrence IDs if there is data returned
for i in response_data['result']['result']['rows']:
    occurrence_id = i[occurrence_column]
    # print('The occurrence ID is: ' + str(occurrence_id))

    # Use the occurence_id to delete occurrences via the API
    url = 'https://api.rollbar.com/api/1/instance/' + str(occurrence_id)
    headers = {
        'X-Rollbar-Access-Token': project_write_token
    }
    payload = {}

    # Do the API call and print out the occurence ID & response
    response = requests.request('DELETE', url, headers=headers, data = payload)
    print('Ocurrence: ' + str(occurrence_id) + ' --- ' + str(response.text.encode('utf8')))


