from optparse import OptionParser 
import urllib
import urllib2
import os
import sys
import xml.dom.minidom
import re
import hashlib
import datetime
import uuid

def loadData(data_path):
    if not os.path.exists(data_path):
        print "file not exits."
        return None
    lines = open(data_path,"r").readlines()
    data_map = {}
    for line in lines:
        if not line.strip() : continue
        if line[0] == "#" : continue
        split_index= line.find ("=")
        if split_index < 0 : continue 
        key = line[0:split_index].strip()
        value = line[split_index+1:].strip()
        data_map[key] = value
    return data_map

def handleValue(data_map):
    pass

def get_now_str():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def get_uuid_str():
    return str(uuid.uuid4())

def get_md5_str(value):
    return hashlib.md5(value).hexdigest() 

def pretty_xml(value):
    xml_obj = xml.dom.minidom.parseString(value) 
    return xml_obj.toprettyxml()

def convert_exp(data_map, v):
    if v.startswith("md5("):
        param = convert_exp(data_map, v.strip()[4:-1])
        v = get_md5_str(param)
    elif v.startswith("date("):
        v = get_now_str()
    elif v.startswith("uuid("):
        v = get_uuid_str()
    elif v.startswith("orderno("):
        param = v.strip()[8:-1]
        v =  param + "_"+ get_uuid_str()
    else :
        pat = re.compile('\$[a-zA-Z_.0-9]+')
        varnames  = pat.findall(v)
        if varnames != None :
            for item in varnames :
                if data_map.get(item[1:]) != None :
                    v = v.replace(item, convert_exp(data_map,data_map.get(item[1:])))
    return v
    

if __name__ == "__main__" :
    description = "post data to url"
    usage="usage: post -u url -d datafile "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)
    parser.add_option('-u','--url', action="store", dest="url")
    parser.add_option('-d','--datafile', action="store", dest="datafile")
    parser.add_option('-f','--format-to-xml', action="store_true", dest="format_to_xml")
    parser.add_option('-p','--print-form-data', action="store_true", dest="print_data")
    (options, args) = parser.parse_args()

    if options.desc :
        print parser.get_description()
        sys.exit(0)

    post_data = loadData(options.datafile)
    for item in post_data :
        value = convert_exp(post_data,post_data[item])
        post_data[item] = value
    if post_data.get("md5") != None:
        post_data.pop("md5")

    if post_data == None :
        sys.exit(0)

    if options.print_data :
        print post_data
        sys.exit(0)


    post_data = urllib.urlencode(post_data)
    page=urllib2.urlopen(options.url, post_data).read().decode("utf-8")

    if options.format_to_xml :
        page = pretty_xml(page)
    print page
