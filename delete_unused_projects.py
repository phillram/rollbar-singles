# coding: utf-8
# _______________________________________________________________
# Deletes Rollbar projects that have never been used 
# (Requires Python 3.6+)
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json

# _______________________________________________________________
# Initializing variables
# Place your Rollbar account read and write tokens here
# _______________________________________________________________
account_read_token = ''
account_write_token = ''


def retrieve_projects():
    """ Retrieves list of projects from a Rollbar account """
    headers = {"X-Rollbar-Access-Token": account_read_token}
    url = "https://api.rollbar.com/api/1/projects"
    response = requests.get(url, headers=headers)
    response_data = response.json()
    # construct a dict of project id and project name
    return {item["id"]: item["name"] for item in response_data["result"]}


def check_project_activity(project_id, project_name):
    """ Checks a project for activity, removing it from the 'projects'
    dict if there's evidence of activity. In this case specifically,
    we're checking if item #1 exists in the project. """
    print(f"Retrieving {project_name:>24}'s read token...", end="")
    project_read_token = retrieve_project_read_token(project_id)
    print(f"checking activity...", end="")
    headers = {"X-Rollbar-Access-Token": project_read_token}
    url = "https://api.rollbar.com/api/1/item_by_counter/1"
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response_data["err"] == 0:
        print("has been used, skipping")
        projects.pop(project_id, None)
    else:
        print("Unused! Prepping to delete.")


def retrieve_project_read_token(project_id):
    """ Retrieves the first project access token with 'read' scope
    given a project ID """
    headers = {"X-Rollbar-Access-Token": account_read_token}
    url = f"https://api.rollbar.com/api/1/project/{project_id}/access_tokens"
    response = requests.get(url, headers=headers)
    response_data = response.json()
    read_tokens = [
        item["access_token"]
        for item in response_data["result"]
        if "read" in item["scopes"]
    ]
    return read_tokens[0]


def delete_unused_project(project_id, project_name):
    """ Deletes a project from Rollbar using the account write token """
    print(f"Deleting {project_name}...", end="")
    headers = {"X-Rollbar-Access-Token": account_write_token}
    url = f"https://api.rollbar.com/api/1/project/{project_id}"
    response = requests.delete(url, headers=headers)
    response_data = response.json()
    if response_data["err"] == 0:
        print("Done!")
        projects.pop(project_id, None)
    else:
        print("error...")

# _______________________________________________________________
# Running the functions above   
# Creates a dict of all projects in a Rollbar account, 
# retrieves their 'read' token, and then checks for activity,
# removing from dict if they've ever been used.
# Then, saves the names and IDs of the unused projects to a .txt file,
# and prompts the user if they'd like to delete them. If there are any
# errors, saves those projects to a separate file.
# _______________________________________________________________
if __name__ == "__main__":
    projects = retrieve_projects()
    
    for k, v in projects.copy().items():
        check_project_activity(k, v)


    print(f"Deleting {len(projects)} projects. Are you sure?")
    print("(Please type 'YES' to proceed, anything else to exit.")
    print("A list of unused projects will be created.)")
    choice = input("> ")
    with open("unused-projects.txt", "a") as f:
        nl = "\n"
        f.writelines([f"{v} - {k}{nl}" for k, v in projects.items()])
    if choice == "YES":
        for k, v in projects.copy().items():
            delete_unused_project(k, v)
        if projects:
            print(f"{len(projects)} projects were unable to be deleted.")
            print("Saving these to 'error.txt'.")
            with open("error.txt", "a") as f:
                nl = "\n"
                f.writelines([f"{v} - {k}{nl}" for k, v in projects.items()])
        else:
            print("Done!")
    else:
        print("Okay. Cancelling!")