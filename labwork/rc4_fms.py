import base64
import requests

session = requests.Session()
def handle_rc4_fms(assignment, api_endpoint, tcid):
    captured_ivs = base64.b64decode(assignment["captured_ivs"])
    key_length = int(assignment["key_length"])

    blocks = [
        captured_ivs[(4 * i):(4 * (i + 1))]
        for i in range(int(len(captured_ivs) / 4))    
    ]
    #print(blocks)

    blocks.sort(key=lambda x: x[0])
    #print(blocks)

    list = {}
    for i in range(len(blocks)):
        if blocks[i][0] not in list:
            list[blocks[i][0]] = []
        list[blocks[i][0]].append(blocks[i])
    #print(groups)

    keys = [[(b'',0)]]

    for i in range(0,key_length):
        possible_keys = keybyte_histogram(list.get(i+3),keys[-1][0][0])
        new_keys = []
        for key in possible_keys:
            new_keys.append( (keys[-1][0][0]+bytes([key[0]]),   
                              key[1]) )
        keys.append(new_keys)
        #print("New keys: ", new_keys)
        #print("Complete keys: ", keys)
    
    for byte in range(key_length+1):

        for how_much_is_the_backtracking in range(0,8):

            key = b''
            for i in range(key_length):
                if byte-1 == i:
                    possible_keys = keybyte_histogram(list.get(i+3),key)
                    key = key + bytes([possible_keys[how_much_is_the_backtracking][0]])
                else:
                    possible_keys = keybyte_histogram(list.get(i+3),key)
                    key = key + bytes([possible_keys[0][0]])

            payload = {"key": base64.b64encode(key).decode("utf-8")}
            request = session.post(api_endpoint + "/submission/" + tcid, headers={"Content-Type": "application/json", "Accept": "application/json"}, json = payload).json()
            if request["status"] == "pass":
                print("Success with: " + base64.b64encode(key).decode("utf-8"))
                session.close()
                return {"key": base64.b64encode(key).decode("utf-8")} 
                     

def keybyte_histogram(blocks, key):
    keys = {}
    blocks.sort(key=lambda x: x[3])

    for block in blocks:
        iv = block
        block = block[0:3]
        keyblock = block + key
        
        sbox = [i for i in range(256)]
        j = 0
        for i in range(int(block[0])):
            j = (j + sbox[i] + keyblock[i]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]

        rbox = [0 for i in range(256)]
        for i in range(256):
            rbox[sbox[i]] = i

        index = (rbox[int(iv[3])] - j - sbox[int(iv[0])]) % 256

        if index not in keys:
            keys[index] = 1
        else:
            keys[index] += 1

    keys = sorted(keys.items(), key=lambda x: x[1], reverse=True)
    #print("Keybyte_Histogram: ", keys)
    return keys
    

    