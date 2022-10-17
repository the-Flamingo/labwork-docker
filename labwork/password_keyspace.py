def handle_keyspace(assignment):
    alphabet = assignment["alphabet"]
    length = assignment["length"]
    restrictions = assignment["restrictions"]

    # A-Z: 65 - 90
    # a-z: 97 - 122
    # 0-9: 48 - 57
    # Special: else

    upper = []
    lower = []
    number = []
    special = []

    for char in alphabet:
        #print("Charakter is: " + char)
        if ord(char) > 64 and ord(char) < 91:
            upper += char
        elif ord(char) > 96 and ord(char) < 123:
            lower += char
        elif ord(char) > 47 and ord(char) < 58:
            number += char
        else:
            special += char
    '''
    print("Alphabet is: " + alphabet)
    print(len(alphabet))
    print(upper, lower, number, special)
    print(len(upper), len(lower), len(number), len(special))
    print(len(upper+lower+number))
    
    at_least_one_special_char (anything but A-Z, a-z and 0-9)
    at_least_one_uppercase_char (A-Z)
    at_least_one_lowercase_char (a-z)
    at_least_one_digit (0-9)
    no_consecutive_same_char (e.g, abcd is permitted but abbc is not)
    special_char_not_last_place (The last character of all the passwords may not be a special character)
    '''

    '''
    count ist len(alphabet)^length
    wenn no_consec_char:
        count ist len(alphabet)*pow(len(alphabet)-1, length-1)
        das erste ist frei, alle anderen sind um das voherige (1) eingeschränkt
    wenn bspw. a.l.o.special:
        gesamtcount muss um die Anzahl der Passwörter reduziert werden, die keine specials enthalten
            aka. len(upper,lower,digit)^length
    '''

    result = pow(len(alphabet), length)
    #print("Base is", result)
    if "no_consecutive_same_char" in restrictions:
        result = len(alphabet)*pow(len(alphabet)-1, length-1)
        #print("CONCHAR changed the result to", result)
    if "at_least_one_special_char" in restrictions:
        result -= pow(len(upper+lower+number),length)
        #print("SPECIAL deducted %i from the result. It's now %i" % (pow(len(upper+lower+number),length),result))
    if "at_least_one_uppercase_char" in restrictions:
        result -= pow(len(lower+number+special),length)
        #print("UPPER deducted %i from the result. It's now %i" % (pow(len(lower+number+special),length),result))
    if "at_least_one_lowercase_char" in restrictions:
        result -= pow(len(upper+number+special),length)
        #print("LOWER deducted %i from the result. It's now %i" % (pow(len(upper+number+special),length),result))
    if "at_least_one_digit" in restrictions:
        result -= pow(len(upper+lower+special),length)
        #print("NUMBER deducted %i from the result. It's now %i" % (pow(len(upper+lower+special),length),result))
    if "special_char_not_last_place" in restrictions:
        result -= pow(len(alphabet), length-1)*len(special)
        #print("LASTSPECIAL deducted %i from the result. It's now %i" % (pow(len(alphabet), length-1)*len(special),result))
    #print("Final is ", result)
    return {"count": result}
    
    