import base64
import math
import random
import hmac
import hashlib

def handle_glasskey(assignment):
    agency_key = int.from_bytes(base64.b64decode(assignment["agency_key"]),byteorder="big")
    e = assignment["e"]
    n = int.from_bytes(base64.b64decode(assignment["n"]),byteorder="big")

    print("")
    p, q = gk_rsa_escrow(agency_key, n)
    phi_n = (p-1) * (q-1)
    #print("Computed phi_n")
    d = pow(e, -1, phi_n)
    print("d:", d)
    #print(base64.b64encode(int.to_bytes(d, length=(round_up(d.bit_length(), 8)//8), byteorder="big")).decode('utf-8'))
    #print("Bitlength d:", d.bit_length())
    #print("Bitlength d//8:", d.bit_length()//8)
    #print("Bitlength d roundup:", round_up(d.bit_length(), 8))
    #print("Bitlength d roundup//8:", round_up(d.bit_length(), 8)//8)
    #print(base64.b64encode(int.to_bytes(d, length=(d.bit_length()//8), byteorder="big")).decode('utf-8'))
    #print(base64.b64encode(int.to_bytes(d, length=(d.bit_length()), byteorder="big")).decode('utf-8'))
    print("base64 d:", base64.b64encode(int.to_bytes(d, length=((round_up(d.bit_length(), 8)//8)), byteorder="big")).decode('utf-8'))
    return {"d": base64.b64encode(int.to_bytes(d, length=((round_up(d.bit_length(), 8)//8)), byteorder="big")).decode('utf-8')}

def gk_drbg(drbg_key, index):
    data = int.to_bytes(index, length=4, byteorder="big")
    #mic = hmac_sha256(key = drbg_key, data = data)
    mic = hmac.new(drbg_key, data, hashlib.sha256).hexdigest()
    #print(mic)
    #print(mic[0:2])
    return mic[0:2]

def gen_bitmask(bitlen):
    assert(bitlen > 0)     
    return (1 << bitlen) - 1

def round_up(bitlen, len):
    for i in range(0,len):
        if (bitlen + i) % len == 0:
            return bitlen + i

def set_bit(num, bit):
    n = 1 << (bit)
    return num | n

def gk_intrg(drbg_key, bitlen):
    values = ""
    #print("Bitlen:", bitlen)
    if (bitlen % 8) != 0:
        #print("Rounding up")
        byte_count = round_up(bitlen, 8) // 8
        #print("Bytecount:", byte_count)
    else:
        byte_count = bitlen // 8
        #print("Bytecount:", byte_count)
    for i in range(byte_count):
        #values.append(gk_drbg(drbg_key, i))
        values += gk_drbg(drbg_key, i)
        #print(values)
    #raw_integer = bytes2integer_big_endian(values)
    raw_integer = int(values, 16)
    #print("")
    #print(raw_integer)
    #print("{:b}".format(raw_integer))
    #print("Lenght:", raw_integer.bit_length())
    bit_mask = gen_bitmask(bitlen)
    #print("BITMASK:")
    #print("{:b}".format(bit_mask))
    #print("Lenght:", bit_mask.bit_length())
    raw_integer &= bit_mask
    #print("")
    #print("{:b}".format(raw_integer))
    #print("Lenght:", raw_integer.bit_length())
    raw_integer = set_bit(raw_integer , bitlen - 1)
    #print("")
    #print("{:b}".format(raw_integer))
    #print("Lenght:", raw_integer.bit_length())
    #print("")
    return raw_integer

def gk_candprime(drbg_key, bitlen):
    raw_integer = gk_intrg(drbg_key, bitlen)
    #raw_integer.set_bit(0)
    #print("{:b}".format(raw_integer))
    raw_integer = set_bit(raw_integer, 0)
    #print("{:b}".format(raw_integer))
    #raw_integer.set_bit(bitlen - 2)
    raw_integer = set_bit(raw_integer, bitlen - 2)
    #print("{:b}".format(raw_integer))
    return raw_integer

def is_prime(n, k=400):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            #print("No Prime")
            return False
    #print("Found Prime")
    return True

def gk_nextprime(value):
    #print("Value:", value)
    value = set_bit(value, 0)
    #print("Value:", value)
    while True:
        #print(value)
        if is_prime(value):
            return value
        value += 2

def gk_primerg(drbg_key, bitlen):
    candidate = gk_candprime(drbg_key, bitlen)
    return gk_nextprime(candidate)

def gk_derive_drbg_key(agency_key, seed):
    assert(isinstance(seed, bytes))
    assert(len(seed) == 8)
    #return sha256_digest(agency_key + seed)
    #print("Agency Key:", agency_key)
    #print("Agency Key Length:", agency_key.bit_length())
    bytes_agency_key = int.to_bytes(agency_key, length = round_up(agency_key.bit_length(), 8) // 8, byteorder="big")
    #print("bytes Agency Key:", bytes_agency_key)
    a_string = bytes_agency_key + seed
    return hashlib.sha256(a_string).digest()

def gk_pgen(drbg_key, modulus_bitlen):
    p_bitlen = modulus_bitlen // 2
    return gk_primerg(drbg_key, p_bitlen)

def gk_p_from_seed(agency_key, seed, modulus_bitlen):
    drbg_key = gk_derive_drbg_key(agency_key, seed)
    #print("gk_p_from_seed.drbg_key:", drbg_key)
    p = gk_pgen(drbg_key, modulus_bitlen)
    return p

def extract_topmost_8_bytes(num):
    bitmask = gen_bitmask(64)
    #n = int.to_bytes(num, length=num.bit_length() // 8, byteorder="big")
    #return int.from_bytes(n[:8], byteorder="big")
    length = num.bit_length() - 64
    bitmask <<= length
    return (num & bitmask) >> length

def gk_rsa_escrow(agency_key, n):
    seed = extract_topmost_8_bytes(n).to_bytes(length = 8, byteorder="big")
    e = 65537
    #print("{:b}".format(n))
    #print("n bitlength:", n.bit_length())
    p = gk_p_from_seed(agency_key, seed, n.bit_length())
    print("p:", p)
    assert((n % p) == 0)
    q = n // p
    print("q:", q)
    return (p, q)