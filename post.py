from optparse import OptionParser 
import urllib
import urllib2
import os
import sys
import xml.dom.minidom

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

def get_now_str():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def get_md5_str(value):
    return hashlib.md5(value).hexdigest() 

def pretty_xml(value):
    xml_obj = xml.dom.minidom.parseString(value) 
    return xml_obj.toprettyxml()
    

if __name__ == "__main__" :
    description = "post data to url"
    usage="usage: post -u url -d datafile "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)
    parser.add_option('-u','--url', action="store", dest="url")
    parser.add_option('-d','--datafile', action="store", dest="datafile")
    parser.add_option('-f','--format-to-xml', action="store_true", dest="format_to_xml")
    (options, args) = parser.parse_args()

    if options.desc :
        print parser.get_description()
        sys.exit(0)

    post_data = loadData(options.datafile)
    if post_data == None :
        sys.exit(0)

    post_data = urllib.urlencode(post_data)
    page=urllib2.urlopen(options.url, post_data).read().decode("utf-8")

    if options.format_to_xml :
        page = pretty_xml(page)
    print page
