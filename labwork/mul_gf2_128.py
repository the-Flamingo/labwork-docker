import base64

def handle_mul_gf2_128(assignment):
    block = assignment["block"]

    bytes_object = base64.b64decode(block)
    #print(bytes_object)

    int_object = int.from_bytes(bytes_object, byteorder="little")
    #print(int_object)

    int_shift = int_object << 1
    #print(int_shift)

    if int_shift & (1 << 128):
        int_shift = int_shift ^ 0x87 
        int_shift = int_shift & ((1 << 128) - 1)
    shift_bytes_object = int.to_bytes(int_shift, byteorder="little", length=16)
    #print(shift_bytes_object)

    result = base64.b64encode(shift_bytes_object).decode('utf-8')
    #print(result)
    return {"block_times_alpha": result}
    #print(result)