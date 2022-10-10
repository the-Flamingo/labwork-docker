#!/usr/bin/python3

def handle_histogram(assignment):
    characters = {}
    for char in assignment["text"]:
        if char in characters:
            characters[char] += 1
        else:
            characters[char] = 1
    return characters
