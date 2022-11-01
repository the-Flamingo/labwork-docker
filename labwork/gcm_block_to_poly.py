import base64

def handle_gcm_block_to_poly(assignment):
    block = base64.b64decode(assignment["block"])
    #print(block)
    #print(block.hex())

    bitarray = "".join(["{:08b}".format(x) for x in block])
    #print(bitarray)

    coefficients = []
    for bit in range(0, len(bitarray)):
        if bitarray[bit] == "1":
            coefficients.append(bit)
    #print(coefficients)

    return {
        "coefficients" : coefficients
    }
