import os
import sys
import re

src_str = sys.argv[1]

def search_ref(src_str):
    result = []
    src_len = len(src_str)
    i = 0
    while True :
        if i >= src_len :
            break
        char = src_str[i]
        if char >= 'A' and char <= 'Z' :
            result.append("_")
            result.append(char.lower())
        elif char == "_" and i < src_len-1:
            i = i + 1
            char = src_str[i]
            result.append(char.upper())
        else :
            result.append(char)
        i = i + 1

    return "".join(result)


if __name__ == "__main__" :
    print search_ref(src_str)
