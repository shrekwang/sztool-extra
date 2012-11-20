import memcache
import sys
import argparse

parser = argparse.ArgumentParser(description='mcache tool')

parser.add_argument('--host', action="store", 
        dest="host", default="127.0.0.1")

parser.add_argument('-p','--port', action="store", 
        dest="port", default="11211" )
parser.add_argument('cmds', nargs='+', default='d')

args_info = parser.parse_args()
conn_str = "%s:%s" % (args_info.host , args_info.port)
mc = memcache.Client([conn_str], debug=0)
cmds = args_info.cmds

if cmds[0] == "get" :
    value = mc.get(cmds[1])
    print value
elif cmds[0] == "del":
    value = mc.delete(cmds[1])
    print "delete %s from cache ok." % cmds[1]
elif cmds[0] == "set":
    mc.set(cmds[1], cmds[2])
    print "set %s into cache ok." % cmds[1]



