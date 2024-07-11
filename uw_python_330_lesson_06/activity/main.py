import sys

import requests

# Use Like python githubber.py JASchilz
# (or another user name)

if __name__ == "__main__":
    try:
        username = sys.argv[1]
        # TODO:
        #
        # 1. Retrieve a list of "events" associated with the given user name
        # 2. Print out the time stamp associated with the first event in that list.
        response = requests.get(
            f"https://api.github.com/users/{username}/events")
        if response.status_code == 404:
            print("User entered does not exist")
        else:
            first_event = response.json()[0]
            print(
                f"Type: {first_event['type']}\nCreated: {first_event['created_at']}")
    except IndexError:
        print("Username wasn't entered")
