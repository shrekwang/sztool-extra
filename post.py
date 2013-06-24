from optparse import OptionParser 
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os
import sys
import re
import hashlib
import datetime
import uuid

def loadData(data_path):
    if not os.path.exists(data_path):
        print "file not exits."
        return {}
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
    soup=BeautifulSoup(value)  
    return soup.prettify()

def convert_exp(data_map, v, v_name = None ):
    if v.startswith("md5("):
        param = convert_exp(data_map, v.strip()[4:-1])
        v = get_md5_str(param)
    elif v.startswith("date("):
        v = get_now_str()
        if v_name != None:
            data_map[v_name] = v
    elif v.startswith("uuid("):
        v = get_uuid_str()
        if v_name != None:
            data_map[v_name] = v
    elif v.startswith("orderno("):
        param = v.strip()[8:-1]
        v =  param + "_"+ get_uuid_str()
        if v_name != None:
            data_map[v_name] = v
    else :
        pat = re.compile('\$[a-zA-Z_.0-9]+')
        varnames  = pat.findall(v)
        if varnames != None :
            for item in varnames :
                v_name = item[1:]
                if data_map.get(v_name) != None :
                    v = v.replace(item, convert_exp(data_map,data_map.get(v_name), v_name))
    return v
    

if __name__ == "__main__" :
    description = "post data to url"
    usage="usage: post -u url -d datafile "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)
    parser.add_option('-u','--url', action="store", dest="url")
    parser.add_option('-c','--cookie', action="store", dest="cookie")
    parser.add_option('-d','--datafile', action="store", dest="datafile")
    parser.add_option('-f','--format-to-xml', action="store_true", dest="format_to_xml")
    parser.add_option('-p','--print-form-data', action="store_true", dest="print_data")
    (options, args) = parser.parse_args()

    if options.desc :
        print parser.get_description()
        sys.exit(0)

    post_data = {}
    if options.datafile != None :
        post_data = loadData(options.datafile)
        for item in post_data :
            value = convert_exp(post_data,post_data[item],item)
            post_data[item] = value
        if post_data.get("md5") != None:
            post_data.pop("md5")

        if post_data == None :
            sys.exit(0)

        if options.print_data :
            print post_data
            sys.exit(0)

    post_data = urllib.urlencode(post_data)
    opener = urllib2.build_opener()
    if options.cookie != None :
        opener.addheaders.append(('Cookie', options.cookie));
    response = opener.open(options.url, post_data)
    content_encoding = "utf-8"
    content_type = response.info().getheader('Content-Type')
    if content_type.strip() :
        content_encoding = content_type[content_type.find("charset")+8:]
        print "encoding is " + content_encoding
    page = response.read().decode(content_encoding,"replace")

    #squeeze empty space
    page = os.linesep.join([s for s in page.splitlines() if s.strip()])
    
    if options.format_to_xml :
        page = pretty_xml(page)
    try :
        #page = page.decode("utf-8")
        page = page.encode(sys.getdefaultencoding(), "ignore")
    except Exception ,e:
        print e
        pass
    print page
