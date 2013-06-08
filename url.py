import sys
from optparse import OptionParser 
import urllib

if __name__ == "__main__" :

    description = "url util"
    usage="usage: url {-e|-d}  url-value "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)
    parser.add_option('-e','--encode', action="store_true", dest="encode")
    parser.add_option('-d','--artifactId', action="store_true", dest="decode")
    parser.add_option('--cp', action="store", dest="cp", default="utf-8")

    (options, args) = parser.parse_args()
    if options.desc :
        print parser.get_description()
        sys.exit(0)
    
    if options.encode :
        print urllib.urlencode({"v":args[0]})[2:]
    elif options.decode:
        codepage = sys.getdefaultencoding()
        print urllib.unquote(args[0]).decode(options.cp).encode(codepage)


