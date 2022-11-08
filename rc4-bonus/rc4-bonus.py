sbox = list(range(256))
print(sbox)

key = []
k = 0
for i in range(256):
    key.append(256 - k)
    k = (k + sbox[i] + key[i]) % 256
print(key) # ==> [256, 256, 255, 254, 253, ..., 2]

#key scheduling
j = 0
for i in range(256):
    j = (j + sbox[i] + key[i % len(key)]) % 256
    #key[] has to counter sbox[] so that j is incrementet only by 1 
    print(sbox[i] + key[i % len(key)])
    #print("Switching (pos/val): ", i, sbox[i], " with ", j, sbox[j])
    (sbox[i], sbox[j]) = (sbox[j], sbox[i])
if sbox == list(range(256)):
    print("Hooray!")

