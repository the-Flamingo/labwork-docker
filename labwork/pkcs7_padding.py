import base64
import requests


session = requests.Session()
def validate_padding(api_endpoint,keyname, iv, cipher):
    
    payload = { "keyname": keyname, 
                "iv": base64.b64encode(iv).decode('utf-8'),
                "ciphertext": base64.b64encode(cipher).decode('utf-8') }
    request = session.post(api_endpoint + "/oracle/pkcs7_padding", headers={"Content-Type": "application/json", "Accept": "application/json"}, json = payload).json()

    if request["status"] == "padding_correct":
        return True
    else: 
        return False


def handle_pkcs7(assignment, api_endpoint):
    print("Ciphertext: " + assignment["ciphertext"])
    cipher = base64.b64decode(assignment["ciphertext"])
    iv = base64.b64decode(assignment["iv"])
    keyname = assignment["keyname"]
    
    blocks = [
        cipher[i:i+16] 
        for i in range(0, len(cipher), 16)
        ]
    plaintext = b''

    for block in blocks:
        dc = bytearray(16 * b'\x00')
        for byte in range(15,-1,-1):
            temp_iv = bytearray(16 * b'\x00')
            for i in range(15, byte, -1):
                forced = 16 - byte
                temp_iv[i] = dc[i] ^ forced
            print("Byte: " + str(byte))
            for i in range(0, 256):
                temp_iv[byte] = i
                if validate_padding(api_endpoint,keyname,temp_iv,block):
                    if byte == 15:
                        temp_cipher = bytearray(block)
                        temp_cipher[-2] = ~temp_cipher[-2] & 0xff
                        if validate_padding(api_endpoint,keyname,temp_iv,temp_cipher):
                            continue
                    dc[byte] = i ^ (16 - byte)
                    
        plaintext += bytes([x ^ y for x, y in zip(iv, dc)])
        iv = block

    print("Plaintext in Hex with Padding: " + plaintext.hex())
    padding = plaintext[-1]
    plaintext = plaintext[:-padding]
    #print("Plaintext in Hex after Paddingremoval: " + plaintext.hex())

    result = base64.b64encode(plaintext).decode("utf-8")
    print("Plaintext: " + result)
    
    return {
        "plaintext": result
    }
