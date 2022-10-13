import base64

assignment = {
        "iv": "AAAAAAAAAAAAAAAAAAAAAA==",
        "key": "AAAAAAAAAAAAAAAAAAAAAA==",
        "operation": "encrypt",
        "opmode": "cbc",
        "plaintext": "VGhpcyBpcyB0aGUgcGxhaW50ZXh0IGV4YW1wbGUgdGhhdCB5b3Ugc2hvdWxkIGVuY3J5cHQgdXNpbmcgQ0JDIHdpdGhvdXQgcGFkZGluZy4="
      }

def handle_block_cipher(assignment):
    opmode = assignment["opmode"]
    operation = assignment["operation"]

    if opmode == "cbc" and operation == "encrypt":
        encypt_cbc(assignment)
    #elif opmode == "cbc" and operation == "decrypt":
        #decypt_cbc()
    #elif opmode == "crt" and operation == "encrypt":
        #encrypt_crt()
    #elif opmode == "crt" and operation == "decrypt":
        #decrypt_crt()
    #elif opmode == "xex" and operation == "encrypt":
        #encrypt_xex()
    #elif opmode == "xex" and operation == "decrypt":
        #decypt_xex()
    else:
        print("Error while handeling Assignment")

def encypt_cbc(assignment):
    key = assignment["key"]
    iv = assignment["iv"]
    plaintext = assignment["plaintext"]

    bytes_iv = base64.b64decode(iv)
    print(bytes_iv)
    int_iv = int.from_bytes(bytes_iv, byteorder="little")
    print(int_iv)

    bytes_plaintext = base64.b64decode(plaintext)
    print(bytes_plaintext)
    int_plaintext = int.from_bytes(bytes_plaintext, byteorder="little")
    print(int_plaintext)

    int_modded = int_plaintext ^ int_iv 
    print(int_modded)

    bytes_modded = int.to_bytes(int_modded, byteorder="little", length=16)
    print(bytes_modded)
    result = base64.b64encode(bytes_modded).decode('utf-8')
    print(result)

handle_block_cipher(assignment)