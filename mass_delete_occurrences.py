# _______________________________________________________________
# Delete all occurrecnces that match an RQL query
# _______________________________________________________________

# _______________________________________________________________
# Imports that are good to use
# _______________________________________________________________
import requests
from time import sleep

# _______________________________________________________________
# Place your project Read/Write API Keys here
# _______________________________________________________________
project_read_token = 'token'
project_write_token = 'token'

# _______________________________________________________________
# Your RQL query
# Copy and paste your working RQL query in between the triple apostrophes
# _______________________________________________________________
query = '''
        SELECT *  
        FROM item_occurrence
        WHERE item.counter = 5
        ORDER BY timestamp DESC
        '''

# Create RQL Job based on the query above
# _______________________________________________________________
def create_rql_search(query):
    url = 'https://api.rollbar.com/api/1/rql/jobs/'

    headers = {
        'X-Rollbar-Access-Token': project_read_token
    }
    payload = {
        'query_string': query, 
            'force_refresh': '1'
        }

    # Doing the API call to create an RQL job
    response = requests.request('POST', url, headers = headers, data = payload)

    # Parse the response to pull the RQL job ID
    # If the RQL query is invalid, stop execution
    response_data = response.json()

    try:
        rql_job_id = response_data['result']['id']
        print('RQL job ID is: ' + str(rql_job_id))
        return rql_job_id
    except:
        print('The RQL job was not created: ' + str(response_data['message']))
        exit()


# Check RQL query results and see if it has completed
# _______________________________________________________________
def retrieve_rql_results(rql_job_id):
    url = 'https://api.rollbar.com/api/1/rql/job/' + str(rql_job_id) + ' /result?expand=job'

    headers = {
        'X-Rollbar-Access-Token': project_read_token
    }
    payload = {}

    retries = 0
    while True:
        # Send the API call and record the response
        response = requests.request('GET', url, headers = headers, data = payload)
        response_data = response.json()

        # Check if the RQL is complete
        rql_status = response_data['result']['job']['status']
        if str(rql_status) == 'success':
            print('RQL job completed')
            return response_data

        # Retry three times with a 10 second pause. Quit after 3 failed attempts
        else:
            print('RQL status is not success. This is try: ' + str(retries))
            sleep(10)
            retries += 1
            if retries >= 3:
                print('RQL status was not success in ' + str(retries) + ' attempts. Quitting.')
                exit()


# Parse the JSON response to pull out the individual occurence_id
# Then delete the occurrences
# _______________________________________________________________
def delete_rql_results(rql_results):
    # Check if there are no results from the RQL query
    if not rql_results['result']['result']['rows']:
        print('There are no occurrences that match your RQL query')
        # Return false to exit the loop
        return False

    # Check what column the occurence ID is
    occurrence_index = 0
    for i in rql_results['result']['result']['columns']:
        # print('RQL column ' + str(occurrence_index) + ' is: ' + str(i))
        if i == 'occurrence_id':
            occurrence_column = occurrence_index
        occurrence_index += 1

    # Pull occurrence IDs if there is data returned
    for i in rql_results['result']['result']['rows']:
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

    # Returns true to restart the main loop outside the function
    return True


# _______________________________________________________________
# Running the functions above   
# Create an RQL query via the API, pull the results,
# parse the results to check if any matches, then delete matches
# _______________________________________________________________
loop = True

while loop:
    # Create RQL search based on the query above, and get the RQL job ID
    rql_job_id = create_rql_search(query)

    # Retreive RQL job status and check if it's success
    rql_results = retrieve_rql_results(rql_job_id)

    # Delete the occurrences matching the RQL results
    loop = delete_rql_results(rql_results)


