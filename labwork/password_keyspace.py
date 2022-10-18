from itertools import product

def handle_keyspace(assignment):
    alphabet = assignment["alphabet"]
    length = assignment["length"]
    restrictions = assignment["restrictions"]

    passwords = ["".join(item) for item in product(alphabet, repeat=length)]
    
    def is_failing_restriction(restriction, password):
        special = []
        upper = []
        lower = []
        number = []

        for char in alphabet:
            if ord(char) > 64 and ord(char) < 91:
                upper += char
            elif ord(char) > 96 and ord(char) < 123:
                lower += char
            elif ord(char) > 47 and ord(char) < 58:
                number += char
            else:
                special += char


        if "at_least_one_special_char" in restriction:
            return not any(char in special for char in password)
        elif "at_least_one_uppercase_char" in restriction:
            return not any(char in upper for char in password)
        elif "at_least_one_lowercase_char" in restriction:
            return not any(char in lower for char in password)
        elif "at_least_one_digit" in restriction:
            return not any(char in number for char in password)
        elif "no_consecutive_same_char" in restriction:
            return any(char == password[index + 1] for index, char in enumerate(password[:-1]))
        elif "special_char_not_last_place" in restriction:
            return password[-1] in special 

    result = 0
    for password in passwords:
        if not any(is_failing_restriction(res, password) for res in assignment["restrictions"]):
            result += 1

    #print(result)
    return {"count": result}
    