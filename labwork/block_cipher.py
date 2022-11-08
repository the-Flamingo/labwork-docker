import base64
import requests
import json
from mul_gf2_128 import handle_mul_gf2_128

block_size = 16
session = requests.Session()

def handle_block_cipher(assignment, endpoint):
    opmode = assignment["opmode"]
    operation = assignment["operation"]

    if opmode == "cbc" and operation == "encrypt":
        return encrypt_cbc(assignment, endpoint)
    elif opmode == "cbc" and operation == "decrypt":
        return decrypt_cbc(assignment, endpoint)
    elif opmode == "ctr":
        return handle_crt(assignment, endpoint)
    elif opmode == "xex" and operation == "encrypt":
        return encrypt_xex(assignment, endpoint)
    elif opmode == "xex" and operation == "decrypt":
        return decrypt_xex(assignment, endpoint)
    else:
        print("Error while handeling Assignment")

def encrypt_cbc(assignment, endpoint):
    iv = assignment["iv"]
    plaintext = assignment["plaintext"]

    bytes_iv = base64.b64decode(iv)
    #print(bytes_iv)
    int_iv = int.from_bytes(bytes_iv, byteorder="little")
    #print(int_iv)

    bytes_plaintext = base64.b64decode(plaintext)
    #print(bytes_plaintext)

    # substring = string[min_char:max_char]
    textblocks = [
        bytes_plaintext[(block_size * i):(block_size * (i + 1))]
        for i in range(int(len(bytes_plaintext) / block_size))    
    ]
    #print(textblocks)

    cipherblocks = []
    payload = {
            "operation": "encrypt",
            "key": assignment["key"],
            "plaintext": base64.b64encode(int.to_bytes(int.from_bytes(textblocks[0], byteorder="little") ^ int_iv, byteorder="little", length=16)).decode('utf-8')
        }
    request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    json_first_cipher = request.json()
    cipherblocks.append( int.from_bytes(base64.b64decode( json_first_cipher["ciphertext"] ), byteorder="little") )
    
    for i in range(1, len(textblocks)):
        payload["plaintext"] = base64.b64encode(int.to_bytes(int.from_bytes(textblocks[i], byteorder="little") ^ cipherblocks[i-1], byteorder="little", length=16)).decode('utf-8')
        request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        json_request = request.json()
        cipherblocks.append(int.from_bytes(base64.b64decode( json_request["ciphertext"] ), byteorder="little"))
    #print(cipherblocks)
    
    bytes_cipherblocks = [
        int.to_bytes(cipherblocks[i], byteorder="little", length=16)
        for i in range(len(cipherblocks))
    ]

    concat = b"".join(bytes_cipherblocks)
    #print({"ciphertext": base64.b64encode(concat).decode('utf-8')})
    result = base64.b64encode(concat).decode('utf-8')
    return {"ciphertext": result}

def decrypt_cbc(assignment, endpoint):
    iv = assignment["iv"]
    ciphertext = assignment["ciphertext"]

    bytes_iv = base64.b64decode(iv)
    int_iv = int.from_bytes(bytes_iv, byteorder="little")

    bytes_ciphertext = base64.b64decode(ciphertext)

    cipherblocks = [
        bytes_ciphertext[(block_size * i):(block_size * (i + 1))]
        for i in range(int(len(bytes_ciphertext) / block_size))    
    ]

    textblocks = []
    payload = {
            "operation": "decrypt",
            "key": assignment["key"],
            "ciphertext": base64.b64encode(int.to_bytes(int.from_bytes(cipherblocks[0], byteorder="little"), byteorder="little", length=16)).decode('utf-8')
        }
    request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    json_first_text = request.json()
    textblocks.append( int.from_bytes(base64.b64decode( json_first_text["plaintext"] ), byteorder="little") ^ int_iv)
    
    for i in range(1, len(cipherblocks)):
        payload["ciphertext"] = base64.b64encode(int.to_bytes(int.from_bytes(cipherblocks[i], byteorder="little"), byteorder="little", length=16)).decode('utf-8')
        request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        json_request = request.json()
        textblocks.append(int.from_bytes(base64.b64decode( json_request["plaintext"] ), byteorder="little") ^ int.from_bytes(cipherblocks[i-1], byteorder="little"))
    #print(textblocks)

    bytes_textblocks = [
        int.to_bytes(textblocks[i], byteorder="little", length=16)
        for i in range(len(textblocks))
    ]

    concat = b"".join(bytes_textblocks)
    result = base64.b64encode(concat).decode('utf-8')
    return {"plaintext": result}

def handle_crt(assignment, endpoint):
    counter = 0
    nonce = base64.b64decode(assignment["nonce"])
    #print(nonce)
    try:
        text = assignment["ciphertext"]
    except:
        text = assignment["plaintext"]
    
    bytes_text = base64.b64decode(text)
    blocks = [
        bytes_text[(block_size * i):(block_size * (i + 1))]
        for i in range(int(len(bytes_text) / block_size))    
    ]

    cipherblocks = []
    for i in range(len(blocks)):
        payload = {
            "operation": "encrypt",
            "key": assignment["key"],
            "plaintext": base64.b64encode((nonce + counter.to_bytes(length=4, byteorder="big"))).decode('utf-8')
        }
        request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        json_first_text = request.json()
        #print(json_first_text)
        cipherblocks.append(int.from_bytes(base64.b64decode(json_first_text["ciphertext"]), byteorder="little") ^ int.from_bytes(blocks[i], byteorder="little"))
        counter += 1

    bytes_cipherblocks = [
        int.to_bytes(cipherblocks[i], byteorder="little", length=16)
        for i in range(len(cipherblocks))
    ]

    concat = b"".join(bytes_cipherblocks)
    result = base64.b64encode(concat).decode('utf-8')
    if "plaintext" in assignment:
        return {"ciphertext": result}
    else:
        return {"plaintext": result}

def encrypt_xex(assignment, endpoint): 
    plaintext = base64.b64decode(assignment["plaintext"])
    bigkey = base64.b64decode(assignment["key"])
    tweak = assignment["tweak"]

    key1 = bigkey[0:16]
    key2 = bigkey[16:32]
    #print(key1, key2)

    payload = { "operation": "encrypt", "key": base64.b64encode(key2).decode('utf-8'), "plaintext": tweak }
    request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload)).json()
    tweak = int.from_bytes(base64.b64decode(request["ciphertext"]), byteorder="little")
    

    textblocks = [
        plaintext[(block_size * i):(block_size * (i + 1))]
        for i in range(int(len(plaintext) / block_size))    
    ]
    #print(textblocks)

    cipherblocks = []
    for i in range(len(textblocks)):
        payload = { "operation": "encrypt", "key": base64.b64encode(key1).decode('utf-8'),
                    "plaintext": base64.b64encode(int.to_bytes(int.from_bytes(textblocks[i], byteorder="little") ^ tweak ,byteorder="little",length=16)).decode('utf-8') }
        request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload)).json()
        #print(request)
        cipherblocks.append(int.to_bytes(int.from_bytes( base64.b64decode(request["ciphertext"]) ,byteorder="little")^tweak ,byteorder="little", length=16))
        times_alpha = handle_mul_gf2_128({"block": base64.b64encode(int.to_bytes(tweak, byteorder="little", length=16))})
        #print("Tweak:", tweak)
        tweak = int.from_bytes( base64.b64decode(times_alpha["block_times_alpha"]) ,byteorder="little")

    concat = b"".join(cipherblocks)
    result = base64.b64encode(concat).decode('utf-8')
    return {"ciphertext": result}

def decrypt_xex(assignment, endpoint):
    ciphertext = base64.b64decode(assignment["ciphertext"])
    bigkey = base64.b64decode(assignment["key"])
    tweak = assignment["tweak"]

    key1 = bigkey[0:16]
    key2 = bigkey[16:32]
    #print(key1, key2)

    payload = { "operation": "encrypt", "key": base64.b64encode(key2).decode('utf-8'), "plaintext": tweak }
    request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload)).json()
    tweak = int.from_bytes(base64.b64decode(request["ciphertext"]), byteorder="little")
    

    cipherblocks = [
        ciphertext[(block_size * i):(block_size * (i + 1))]
        for i in range(int(len(ciphertext) / block_size))    
    ]
    #print(cipherblocks)

    textblocks = []
    for i in range(len(cipherblocks)):
        payload = { "operation": "decrypt", "key": base64.b64encode(key1).decode('utf-8'),
                    "ciphertext": base64.b64encode(int.to_bytes(int.from_bytes(cipherblocks[i], byteorder="little") ^ tweak ,byteorder="little",length=16)).decode('utf-8') }
        request = session.post(endpoint + "/oracle/block_cipher", headers={"Content-Type": "application/json"}, data=json.dumps(payload)).json()
        #print(request)
        textblocks.append(int.to_bytes(int.from_bytes( base64.b64decode(request["plaintext"]) ,byteorder="little")^tweak ,byteorder="little", length=16))
        times_alpha = handle_mul_gf2_128({"block": base64.b64encode(int.to_bytes(tweak, byteorder="little", length=16))})
        #print("Tweak:", tweak)
        tweak = int.from_bytes( base64.b64decode(times_alpha["block_times_alpha"]) ,byteorder="little")

    concat = b"".join(textblocks)
    result = base64.b64encode(concat).decode('utf-8')
    return {"plaintext": result}