import sys
import json
import requests
from strcat import handle_strcat
from histogram import handle_histogram
from caesar_cipher import handle_caesar

if len(sys.argv) != 4:
    print("syntax: %s [API endpoint URI] [client ID] [assignment_name]" % (sys.argv[0]))
    sys.exit(1)

api_endpoint = sys.argv[1]
client_id = sys.argv[2]
assignment_name = sys.argv[3]

session = requests.Session()
# Get the assignment
result = session.get(api_endpoint + "/assignment/" + client_id + "/" + assignment_name)
assert (result.status_code == 200)

# See if we can compute the answer
assignment = result.json()

for testcase in assignment["testcases"]:
    if testcase["type"] == "strcat":
        response = handle_strcat(testcase["assignment"])
    elif testcase["type"] == "histogram":
        response = handle_histogram(testcase["assignment"])
    elif testcase["type"] == "caesar_cipher":
        response = handle_caesar(testcase["assignment"])
    else:
        print("Do not know how to handle type: %s" % (testcase["type"]))
        continue

    # We think we have an answer for this one, try to submit it
    result = session.post(api_endpoint + "/submission/" + testcase["tcid"], headers={"Content-Type": "application/json"}, data=json.dumps(response))
    assert (result.status_code == 200)
    submission_result = result.json()
    if submission_result["status"] == "pass":
        print("Passed a test! %s" % (testcase["type"]))
    else:
        print(submission_result)

