def handle_caesar(assignment):
    action = assignment["action"]
    #print("Recieved Assignment. Action is %s" % action)
    if action == "encrypt":
        #print("Encrypting...")
        return encrypt(assignment)
    elif action == "decrypt":
        #print("Decrypting...")
        return decrypt(assignment)
    else:
        print("Unexpected action while handling caesar: %s" % action)


def encrypt(assignment):
    result = ""
    plaintext = assignment["plaintext"]
    letter_shift = assignment["letter_shift"]
    #print("Recieved Plaintext \"%s\" and Shift \"%i\"" % (plaintext, letter_shift))

    for i in range(0, len(plaintext)):
        char = plaintext[i]
        #print("Got letter \"%s\" with ord \"%i\"" % (char, ord(char)))
        if ord(char) < 65 or 90 < ord(char) < 97 or ord(char) > 122:
            #print("!!! Char was skipped!")
            result += char
            continue

        if char.isupper():
            result += chr((ord(char) + letter_shift - 65) % 26 + 65)
            #print("With %i Shift it becomes %s" % (letter_shift, result))
        else:
            result += chr((ord(char) + letter_shift - 97) % 26 + 97)
            #print("With %i Shift it becomes %s" % (letter_shift, result))
        #print(result)
    return result


def decrypt(assignment):
    result = ""
    ciphertext = assignment["ciphertext"]
    letter_shift = assignment["letter_shift"]
    #print("Recieved Ciphertext \"%s\" and Shift \"%i\"" % (ciphertext, letter_shift))

    for i in range(0, len(ciphertext)):
        char = ciphertext[i]
        if ord(char) < 65 or 90 < ord(char) < 97 or ord(char) > 122:
            result += char
            continue

        if char.isupper():
            result += chr((ord(char) - letter_shift - 65) % 26 + 65)
        else:
            result += chr((ord(char) - letter_shift - 97) % 26 + 97)
    #print(result)
    return result
