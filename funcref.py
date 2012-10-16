import os
import sys
import re

html_file_path = sys.argv[1]
func_name = sys.argv[2]

#html_file_path = r"D:\work\kedou\src\main\webapp\back\card\cardApply\list_cardApply_back.html"
#func_name = "showAdd"

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
    search_ref(html_file_path, func_name)
