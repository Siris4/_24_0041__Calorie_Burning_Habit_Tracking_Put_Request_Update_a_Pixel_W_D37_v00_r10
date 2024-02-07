import requests
import json
from datetime import datetime
import os

USERNAME = os.environ.get('USERNAME')    #the API Key from the open weather website
print(f"The USERNAME is: {USERNAME}")

TOKEN = os.environ.get('TOKEN')    #the API Key from the open weather website
print(f"The TOKEN is: {TOKEN}")

GRAPH_NAME = "graph1"

# Step 1):

pixela_endpoint = "https://pixe.la/v1/users"  # everything before the space and -d

'''
token	string	[required] A token string used to authenticate as a user to be created. The token string is hashed and saved.
Validation rule: [ -~]{8,128}
username	string	[required] User name for this service.
Validation rule: [a-z][a-z0-9-]{1,32}
agreeTermsOfService	string	[required] Specify yes or no whether you agree to the terms of service.
Please see: Terms of service - Japanese version / Terms of service - English version
notMinor	string	[required] Specify yes or no as to whether you are not a minor or if you are a minor and you have the parental consent of using this service.
'''

user_params = {
    "token": TOKEN,  # user generated, so make it up yourself.
    "username": USERNAME,     # pick a username. Let's stay consistent with the dev account naming convention, but no periods in the username.
    "agreeTermsOfService": "yes",   # remember that Keys have to be IDENTICAL to any and all CAPS involved, so copy and paste Key names.
    "notMinor": "yes",   # 4 total service agreements to POST a request, up to this point
}

# pixela_response = requests.post(url=pixela_endpoint, json=user_params)
# print(pixela_response.text)  # give it back to me in a peice of text, instead of JSON format, which we just want to visually see it quickly, so no need to keep in JSON for now, if data manipulation is not being done with it.
# print(pixela_response.json)  # if you really do want the data back in a JSON format.
#{"message":"Success. Let's visit https://pixe.la/@siris1dev , it is your profile page!","isSuccess":true}
#<bound method Response.json of <Response [200]>>

# If you run it a second time:
#{"message":"This user already exist.","isSuccess":false}
#<bound method Response.json of <Response [409]>>

# Step 2): $ curl -X POST https://pixe.la/v1/users/a-know/graphs -H 'X-USER-TOKEN:thisissecret' -d '{"id":"test-graph","name":"graph-name","unit":"commit","type":"int","color":"shibafu","timezone":"Asia/Tokyo","isSecret":true,"publishOptionalData":true}'
# {"message":"Success.","isSuccess":true}

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

# [required] It is an ID for identifying the pixelation graph.
# Validation rule: ^[a-z][a-z0-9-]{1,16}
graph_config = {    #similar to params, but for the graph part of the POST REQUEST:
    "id": GRAPH_NAME,
    "name": "Calorie Burning Graph",
    "unit": "calorie(s)",
    "type": "int",    # integer type for calories
    "color": "sora"   # (blue color, in their Japanese variable names)
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# Make another POST REQUEST within the HEADER:
# graph_response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(graph_response.text)
#{"message":"This graphID already exist."

# POST /v1/users/<username>/graphs/<graphID>:

# Required:
# TODO: X-USER-TOKEN is the TOKEN Constant

# TODO: 'date' in yyyyMMdd format, to be registered
# TODO: 'quantity' to be registered
# TODO: (in JSON string, 'optionalData' to have additional info recorded for the date).

#If we want to change today's Timestamped date, and THEN reformat it to be in the format that it preferred (YYYYMMDD), we would use strftime("%Y%m%d"):
today = datetime.now()
print(today)

# If we wanted to backtrack our date to a previous day, we could do this:
custom_date = datetime(year=2024, month=1, day=29)
custom_date_formatted = custom_date.strftime("%Y%m%d")

# $ curl -X POST https://pixe.la/v1/users/a-know/graphs/test-graph -H 'X-USER-TOKEN:thisissecret' -d '{"date":"20180915","quantity":"5","optionalData":"{\"key\":\"value\"}"}'
posting_a_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_NAME}/{custom_date_formatted}"   # update our endpoint URL, by adding what we had previously, but add "/graphs/graph1"

# [required] It is an ID for identifying the pixelation graph.
# Validation rule: ^[a-z][a-z0-9-]{1,16}
# posting_a_pixel_config = {    #similar to params, but for the graph part of the POST REQUEST:
#     "id": "graph1",
#     "name": "Calorie Burning Graph",
#     "unit": "calorie(s)",
#     "type": "int",
#     "color": "sora"   # (blue color, in their Japanese variable names)
# }

headers = {
    "X-USER-TOKEN": TOKEN
}

# Make another POST REQUEST within the HEADER:
# graph_response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(graph_response.text)
#{"message":"This graphID already exist."



# But it prints out like: 2024-01-31 02:08:06.815155
# we need for it to be in a different format. We could use the from datetime import datetime method, and use the "string f time method" = strftime() Method.
# https://www.geeksforgeeks.org/python-strftime-function/
todays_formatted_date = today.strftime("%Y%m%d")
print(todays_formatted_date)

posting_a_pixel_config = {
    "date": custom_date_formatted,  #format: YYYYMMDD
    "quantity": "0",   # in calories
    "optionalData": json.dumps("Walk/hike at a nearby park")   # dumps, with an s, to indicate it should be a json STRING format/
}

#   https://pixe.la/v1/users/a-know/graphs/test-graph
#   POST https://pixe.la/v1/users/a-know/graphs/test-graph -H 'X-USER-TOKEN:thisissecret' -d '{"date":"20180915","quantity":"5","optionalData":"{\"key\":\"value\"}"}'
posting_a_pixel_response = requests.put(url=posting_a_pixel_endpoint, json=posting_a_pixel_config, headers=headers)
print(posting_a_pixel_response.text)
#{"message":"Success.","isSuccess":true}

# GPT Help for POST: Posting a Pixel:
'''
import json

# Correct URL for posting a pixel
posting_a_pixel_endpoint = f"{pixela_endpoint}/v1/users/{USERNAME}/graphs/graph1"

# Correct headers (TOKEN is already included here)
headers = {
    "X-USER-TOKEN": TOKEN
}

# Correct configuration for posting a pixel
posting_a_pixel_config = {
    "date": "20240130",
    "quantity": "323",
    "optionalData": json.dumps({"note": "walk/hike with Bets at a nearby park that Bets likes"})
}

# Correct POST request
posting_a_pixel_response = requests.post(url=posting_a_pixel_endpoint, json=posting_a_pixel_config, headers=headers)
print(posting_a_pixel_response.text)
'''

#{"message":"Success.","isSuccess":true}