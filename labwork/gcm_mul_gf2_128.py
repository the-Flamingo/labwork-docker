import base64

def handle_gcm_mul_gf2_128(assignment):
    #print("")
    #print("a: ", assignment["a"])
    #print("b: ", assignment["b"])
    a = base64.b64decode(assignment["a"])
    b = base64.b64decode(assignment["b"])
    r = base64.b64decode("4QAAAAAAAAAAAAAAAAAAAIA=") 
                                          # 11100001 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 1000000
    handable_a = gcm_to_handable(a)
    handable_b = gcm_to_handable(b)
    handable_r = gcm_to_handable(r)
    
    int_a = int.from_bytes(handable_a, byteorder="big")
    int_b = int.from_bytes(handable_b, byteorder="big")
    int_r = int.from_bytes(handable_r, byteorder="big")
    #print("a= ", handable_a)
    #print("bitlen a= ", int.bit_length(int_a))
    #print("b= ", handable_b)
    #print("bitlen b= ", int.bit_length(int_b))
    #print("r= ", handable_r)
    #print("bitlen r= ", int.bit_length(int_r))

    # Generate xor table
    xortable = []
    for bit in range(int.bit_length(int_a)):
        if get_bit(int_a, bit) == 1:
            bytes_b = int.to_bytes(int_b, byteorder="big", length=32)
            #print(bytes_b)
            xortable.append(bytes_b)
        int_b = int_b << 1
    #print(xortable)

    # ^ all contents to xor
    xor = (32 * b'\x00')
    int_xor = int.from_bytes(xor, byteorder='big')
    for item in xortable:
        int_item = int.from_bytes(item, byteorder="big")
        int_xor = int_xor ^ int_item
    xor = int.to_bytes(int_xor, byteorder="big", length=32)
    #print("xor after mult= ", xor)
    #print("Bitlen xor= ", int.bit_length(int_xor))

    while int.bit_length(int_xor) >= int.bit_length(int_r):
        shift = int.bit_length(int_xor) - int.bit_length(int_r)
        #print("Shift= ", shift)
        temp_int_r = int_r << shift
        #print("Temp_r=      ", int.to_bytes(temp_int_r, byteorder="big",length=32))
        int_xor = int_xor ^ temp_int_r
        #print("Current xor= ", int.to_bytes(int_xor, byteorder="big",length=32))
        #print("Bitlen xor=  ", int.bit_length(int_xor))
    bytes_xor = int.to_bytes(int_xor, byteorder="big", length=16)    
        

    #cut = bytes_xor[-16:]
    #print("Try cutting: ", cut)

    gcm = gcm_to_handable(bytes_xor)
    #print(gcm)

    result = base64.b64encode(gcm).decode('utf-8')
    #print("Base64 Result: ", result)

    return {
        "a*b": result
        }

def get_bit(number, position):
    # Give the number as static input and store it in a variable.
    gvn_numb = number
    # Give the bit position that you need to get the bit value at that position as static input
    # and store it in another variable.
    bitpositin = position
    # Apply the left shift operator to 1 and the above-given bit position and
    # store it in another variable.
    numbr_bit = (1 << bitpositin)
    # Apply bitwise & operation for the given number and the above result and
    # store it in another variable say bit_val.
    bit_val = gvn_numb & numbr_bit
    # Check if the above result bit_val is greater than 0 using the if conditional statement.
    if (bit_val > 0):
        # If the statement is true, then print "The bit present at the given position is 1".
        return 1
    else:
        return 0

def gcm_to_handable(bytearray):
    result = b''
    for byte in range(len(bytearray)-1, -1, -1):
        result += int.to_bytes((reverse_Bits(bytearray[byte], 8)), length=1, byteorder='big')
    return result
        

def reverse_Bits(n, no_of_bits):
    result = 0
    for i in range(no_of_bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result
    