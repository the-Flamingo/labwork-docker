#!/usr/bin/python3

import sys
import json
import requests
from strcat import handle_strcat
from histogram import handle_histogram
from caesar_cipher import handle_caesar
from password_keyspace import handle_keyspace
from mul_gf2_128 import handle_mul_gf2_128
from block_cipher import handle_block_cipher
from pkcs7_padding import handle_pkcs7
from cbc_key_equals_iv import handle_cbc_key_equals_iv
from gcm_block_to_poly import handle_gcm_block_to_poly
from gcm_mul_gf2_128 import handle_gcm_mul_gf2_128
from rc4_fms import handle_rc4_fms
from chi_square import handle_chi_square
from timing_sidechannel import handle_timing_sidechannel
from rsa_crt_fault_injection import handle_rsa_crt_fault_injection
from glasskey import handle_glasskey

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
unknown_assignment_count = 0
pass_count = 0
for testcase in assignment["testcases"]:
    if testcase["type"] == "strcat":
        response = handle_strcat(testcase["assignment"])
    elif testcase["type"] == "histogram":
        response = handle_histogram(testcase["assignment"])
    elif testcase["type"] == "caesar_cipher":
        response = handle_caesar(testcase["assignment"])
    elif testcase["type"] == "password_keyspace":
        response = handle_keyspace(testcase["assignment"])
    elif testcase["type"] == "mul_gf2_128":
        response = handle_mul_gf2_128(testcase["assignment"])
    elif testcase["type"] == "block_cipher":
        response = handle_block_cipher(testcase["assignment"], api_endpoint)
    elif testcase["type"] == "pkcs7_padding":
        response = handle_pkcs7(testcase["assignment"], api_endpoint)
    elif testcase["type"] == "cbc_key_equals_iv":
        response = handle_cbc_key_equals_iv(testcase["assignment"], api_endpoint)
    elif testcase["type"] == "gcm_block_to_poly":
        response = handle_gcm_block_to_poly(testcase["assignment"])
    elif testcase["type"] == "gcm_mul_gf2_128":
        response = handle_gcm_mul_gf2_128(testcase["assignment"])
    elif testcase["type"] == "rc4_fms":
        response = handle_rc4_fms(testcase["assignment"], api_endpoint, testcase["tcid"])
    elif testcase["type"] == "chi_square":
        response = handle_chi_square(testcase["assignment"])
    elif testcase["type"] == "timing_sidechannel":
        response = handle_timing_sidechannel(testcase["assignment"], api_endpoint)
    elif testcase["type"] == "rsa_crt_fault_injection":
        response = handle_rsa_crt_fault_injection(testcase["assignment"])
    elif testcase["type"] == "glasskey":
        response = handle_glasskey(testcase["assignment"])
    else:
        print("Do not know how to handle type: %s" % (testcase["type"]))
        unknown_assignment_count += 1
        continue

    # We think we have an answer for this one, try to submit it
    result = session.post(api_endpoint + "/submission/" + testcase["tcid"], headers={"Content-Type": "application/json"}, data=json.dumps(response))
    assert (result.status_code == 200)
    submission_result = result.json()
    if submission_result["status"] == "pass":
        print("Passed a test! %s" % (testcase["type"]))
        pass_count += 1
    else:
        print(submission_result)
print("%d assignments passed, %d unknown." % (pass_count, unknown_assignment_count))