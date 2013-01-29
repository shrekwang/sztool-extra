import os
import sys
import re
from optparse import OptionParser 


def convert_camel(values):
    result = []
    src_len = len(values)
    i = 0
    while True :
        if i >= src_len :
            break
        char = values[i]
        if char >= 'A' and char <= 'Z' :
            result.append("_")
            result.append(char.lower())
        elif char == "_" and i < src_len-1:
            i = i + 1
            char = values[i]
            result.append(char.upper())
        else :
            result.append(char)
        i = i + 1

    return "".join(result)


if __name__ == "__main__" :
    description = "  convert camelcase string to '_' splited string and vice verse"
    usage="usage: camel value [values..]"
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)

    (options, args) = parser.parse_args()
    if options.desc :
        print parser.get_description()
        sys.exit(0)

    values = " ".join(args)
    if len(args) < 1: 
        parser.print_help()
        sys.exit(0)
    
    print convert_camel(values)
