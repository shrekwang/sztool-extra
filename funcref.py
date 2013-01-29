import os
import sys
import re
from optparse import OptionParser 

pat = re.compile("""<script type="text/javascript" src="(?P<src>.*)"></script>""")

def search_ref(html_file_path, func_name):
    if not os.path.exists(html_file_path) :
        print "html file not exits."
        return

    dirname = os.path.dirname(html_file_path)

    lines = open(html_file_path).readlines()
    for line in lines :
        result = pat.search(line)
        if result != None :
            src = result.group("src")
            src = os.path.normpath(os.path.join(dirname, src))
            if os.path.exists(src):
                content = open(src).readlines()
                matched_lines = {}
                for rownum, item in enumerate(content):
                    if func_name in item :
                        matched_lines[rownum] = item
                if len(matched_lines) > 0 :
                    print src + ":"
                    for rownum in matched_lines :
                        print "     " + str(rownum) + ":" + matched_lines[rownum]


if __name__ == "__main__" :
    description = " find out where did the javascrifpt function was defined "
    usage="usage: funcref html_file js_func_name"
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)

    (options, args) = parser.parse_args()
    if options.desc :
        print parser.get_description()
        sys.exit(0)

    if len(args) < 2 :
        parser.print_help()
        sys.exit(0)

    html_file_path = args[0]
    func_name = args[1]
    search_ref(html_file_path, func_name)
