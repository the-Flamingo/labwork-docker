import base64
import hashlib
import math

def handle_rsa_crt_fault_injection(assignment):

    print("")
    e = int.from_bytes(base64.b64decode(assignment['pubkey']['e']), byteorder='big')
    #print("e:", e)
    n = int.from_bytes(base64.b64decode(assignment['pubkey']['n']), byteorder='big')
    #print("n:", n)

    msg = base64.b64decode(assignment['msg'])
    print("msg:", msg)
    md5sum = hashlib.md5(msg).digest()
    #print("md5sum:", md5sum)
    int_msg = int.from_bytes(
        (   b'\x01' 
          + b'\xff' * (math.ceil(n.bit_length() / 8) - len(md5sum) - 2) 
          + b'\x00' 
          + md5sum),
        byteorder='big'
        )
    #print("int_msg:", int_msg)

    sigs = [
        int.from_bytes(base64.b64decode(assignment['sigs'][0]), byteorder='big'),
        int.from_bytes(base64.b64decode(assignment['sigs'][1]), byteorder='big')
        ]

    sig = pow(sigs[0], e, n)
    if sig == int_msg:
        sig = pow(sigs[1], e, n)
    #print("sig:", sig)

    p = math.gcd(sig - int_msg, n)
    #print("p:", p)
    q = n // p
    #print("q:", q)
    d = pow(e, -1, (p-1)*(q-1))
    #print("d:", d)

    if q < p: 
        q, p = p, q

    d_tosend = base64.b64encode(
                        d.to_bytes(
                            math.ceil(d.bit_length() / 8),
                            byteorder='big')
                                ).decode('utf-8')
    print("d to send:", d_tosend)
    p_tosend = base64.b64encode(p.to_bytes(math.ceil(p.bit_length() / 8) , byteorder='big')).decode('utf-8')
    print("p to send:", p_tosend)
    q_tosend = base64.b64encode(q.to_bytes(math.ceil(q.bit_length() / 8) , byteorder='big')).decode('utf-8')
    print("q to send:", q_tosend)

    return { "d": d_tosend, "p": p_tosend, "q": q_tosend }

