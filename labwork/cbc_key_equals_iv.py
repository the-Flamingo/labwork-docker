import base64
import requests

session = requests.Session()
def handle_cbc_key_equals_iv(assignment, endpoint):
    #print("")
    valid_ciphertext = base64.b64decode(assignment["valid_ciphertext"])
    keyname = assignment["keyname"]

    cipherblocks = [
        valid_ciphertext[(16 * i):(16 * (i + 1))]
        for i in range(int(len(valid_ciphertext) / 16))    
    ]
    #print(cipherblocks)

    cipherblocks.append(cipherblocks[-2])
    cipherblocks.append(cipherblocks[-2])
    #print(cipherblocks)

    cipherblocks[1] = 16 * b'\x00'
    #print(cipherblocks)
    cipherblocks[2] = cipherblocks[0]
    #print(cipherblocks)

    cipher = b''.join(cipherblocks)
    #print(cipher)

    payload = { "keyname": keyname, 
                "ciphertext": base64.b64encode(cipher).decode('utf-8') 
            }
    request = session.post(endpoint + "/oracle/cbc_key_equals_iv", headers={"Content-Type": "application/json", "Accept": "application/json"}, json = payload).json()
    plaintext = base64.b64decode(request["plaintext"])
    #print(plaintext)

    key = bytes([x ^ y for x, y in zip(plaintext[0:16], plaintext[32:48])])
    #print(base64.b64encode(key).decode('utf-8'))
    
    return {
        "key": base64.b64encode(key).decode('utf-8')
    }
