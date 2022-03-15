# _______________________________________________________________
# Get all occurrence details for a given Rollbar item
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json, time

# _______________________________________________________________
# Initializing variables
# Place your Rollbar access token and item counter here
# _______________________________________________________________
account_read_token = ''

# Counter of the item you're trying to pull occurrences (this is the item number in the UI)
item_counter = ''

# If you know the occurrence ID you want to start at, place it here. Otherwise, leave as None
last_occurrence_id = None

# Set to True to create a local file of occurrence data
make_file = False

# _______________________________________________________________
# Get item ID using the item counter above
# _______________________________________________________________
def retrieve_item_id(item_counter):
    headers = {
        'X-Rollbar-Access-Token': account_read_token
    }

    payload = {}

    url = 'https://api.rollbar.com/api/1/item_by_counter/' + str(item_counter)

    response = requests.request('GET', url, headers = headers, data = payload)

    # Parse the response to JSON
    response_data = response.json()

    # Getting a list of the project IDs
    rollbar_item_id = response_data['result']['id']

    return rollbar_item_id

# _______________________________________________________________
# Retrieve occurrence information
# _______________________________________________________________
def get_occurrences(rollbar_item_id, last_occurrence_id):
    headers = {
        'X-Rollbar-Access-Token': account_read_token
    }

    payload = {}

    url = 'https://api.rollbar.com/api/1/item/' + str(rollbar_item_id) + '/instances?lastId=' + str(last_occurrence_id)

    response = requests.request('GET', url, headers = headers, data = payload)
    
    # Parse the response to JSON
    response_data = response.json()
    
    # Check if any data is returned, if not, let's end the loop
    if len(response_data['result']['instances']) == 0: 
        print('There are no more occurrences')
        return 'data_finished'

    # If there is data, then let's parse those
    for i in response_data['result']['instances']:
        last_occurrence_id = i['id']
        print(str(i))

        # Write to file if necessary
        if make_file:
            occurrence_file.write(str(i) + "\n")

    return last_occurrence_id

# _______________________________________________________________
# Running the functions above   
# Find the ID of your item, then pull the occurrence data
# Optionally add this data to a document
# _______________________________________________________________

# Create file to store occurrence data
if make_file:
    occurrence_file = open('occurrence_data.txt', 'w')

# Get item ID from counter
rollbar_item_id = retrieve_item_id(item_counter)
print('Item ID: ' + str(rollbar_item_id))

# Get occurrence data using item ID
while not last_occurrence_id == 'data_finished':
    last_occurrence_id = get_occurrences(rollbar_item_id, last_occurrence_id)
    print('Last occurrence ID is: ' + str(last_occurrence_id))

# Close file to store occurrence data
if make_file:
    occurrence_file.close()

