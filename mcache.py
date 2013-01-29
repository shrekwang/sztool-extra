import memcache
import sys
from optparse import OptionParser 


description = "memcached client utilty"
usage="usage: mcache {get|del|set} arguments "
parser = OptionParser(description = description, usage = usage)
parser.add_option("--desc",action="store_true", dest="desc", default=False)
parser.add_option('--host', action="store", dest="host", default="127.0.0.1")
parser.add_option('-p','--port', action="store", dest="port", default="11211" )

(options, args) = parser.parse_args()
if options.desc :
    print parser.get_description()
    sys.exit(0)

args_info = parser.parse_args()
conn_str = "%s:%s" % (options.host , options.port)
mc = memcache.Client([conn_str], debug=0)

if args[0] == "get" :
    value = mc.get(args[1])
    print value
elif args[0] == "del":
    value = mc.delete(args[1])
    print "delete %s from cache ok." % args[1]
elif args[0] == "set":
    mc.set(args[1], args[2])
    print "set %s into cache ok." % args[1]



