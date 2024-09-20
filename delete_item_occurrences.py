# _______________________________________________________________
# Delete all occurrecnces in an item
# _______________________________________________________________

# _______________________________________________________________
# Imports that are good to use
# _______________________________________________________________
import requests
from time import sleep

# _______________________________________________________________
# Place your project Read/Write API Keys here
# Add your Rollbar item counter. This is the number in the UI.
# _______________________________________________________________
project_read_token = 'token'
project_write_token = 'token'
rollbar_item_counter = 'number'

# Pull the item ID based on the counter
# _______________________________________________________________
def get_item_id(rollbar_item_counter):
    url = 'https://api.rollbar.com/api/1/item_by_counter/' + str(rollbar_item_counter)

    headers = {
        'X-Rollbar-Access-Token': project_read_token
    }
    payload = {}

    # Doing the API call to get item information
    response = requests.request('GET', url, headers = headers, data = payload)

    # Parse the response to pull the item ID
    # If an error happens, stop execution
    response_data = response.json()
    
    try:
        item_id = response_data['result']['id']
        print('Item ID: ' + str(item_id))
        return item_id
    except:
        print('The item data was not found with error: ' + str(response_data['message']))
        exit()


# Pull list of all occurrences in the item
# _______________________________________________________________
def delete_occurrences(item_id):
    url = 'https://api.rollbar.com/api/1/item/' + str(item_id) + '/instances?limit=5000'

    headers = {
        'X-Rollbar-Access-Token': project_read_token
    }

    payload = {}

    # Doing the API call to get information
    response = requests.request('GET', url, headers=headers, data=payload)

    # Parse the response to loop through the occurrence IDs
    response_data = response.json()

    # If there are no occurrences, stop the execution
    if response_data['result']['instances'] == []:
        return

    for i in response_data['result']['instances']:
        occurrence_id = i['id']

        # Delete the occurence
        url = 'https://api.rollbar.com/api/1/instance/' + str(occurrence_id)
        headers = {
            'X-Rollbar-Access-Token': project_write_token
        }
        payload = {}

        response = requests.request('DELETE', url, headers = headers, data = payload)
        status = response.status_code
        if status == 200:
            print('Deleted Occurrence ID: ' + str(occurrence_id))
        else:
            print('Deletion is failed. Occurrence ID: ' + str(occurrence_id))

    # call next page
    delete_occurrences(item_id)

# _______________________________________________________________
# Running the functions above
# _______________________________________________________________

# Get the item ID from the counter
item_id = get_item_id(rollbar_item_counter)

# Delete the occurrences within the item
delete_occurrences(item_id)
