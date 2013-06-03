import sys
import os.path
import os
from subprocess import Popen
from xml.etree.ElementTree import *
from optparse import OptionParser 

M2_REPO="D:/repo"


def getProjectCfg():
    user_home = os.path.expanduser('~')
    project_cfg_path = os.path.join(user_home,".sztools/project.cfg")
    if not os.path.exists(project_cfg_path):
        return
    lines = open(project_cfg_path,"r").readlines()
    cfg_dict = {}
    for line in lines:
        if not line.strip() : continue
        if line[0] == "#" : continue
        split_index= line.find ("=")
        if split_index < 0 : continue 
        key = line[0:split_index].strip()
        value = line[split_index+1:].strip()
        cfg_dict[key] = value
    return cfg_dict


def getProjectWebClassPath():
    tree = ElementTree()
    project_cfg = getProjectCfg()

    classPathXmlPath = os.path.join(os.getcwd(), ".tomcatplugin")
    if not os.path.exists(classPathXmlPath):
        return None
    
    tree.parse(classPathXmlPath)
    entries = tree.findall("webClassPathEntries/webClassPathEntry")
    cp_entries = []
    for entry in  entries :
        path = entry.text
        if "M2_REPO" in path:
            path = path.replace("M2_REPO",M2_REPO)
        elif path.startswith("/"):
            prj_name , inner_path = path[1:].split("/",1)
            prj_ab_path = project_cfg.get(prj_name)
            if prj_ab_path == None :
                print "can't find project '%s' config in project.cfg " % (prj_name)
                sys.exit(0)
            path = os.path.normpath(os.path.join(prj_ab_path, inner_path))
        path = os.path.normpath(path)
        cp_entries.append(path)

    return cp_entries

if __name__ == "__main__" :

    description = "generate .#webclasspath used by sysdeo plugin class loader"
    usage="usage: webcp "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)

    (options, args) = parser.parse_args()
    if options.desc :
        print parser.get_description()
        sys.exit(0)

    projectClassPath = getProjectWebClassPath()
    if projectClassPath == None :
        projectClassPath =[]
    
    webclasspath_file = open("src/main/webapp/.#webclasspath","w")
    for item in projectClassPath :
        webclasspath_file.write(item+"\n")
    webclasspath_file.close()

    print ".#webclasspath file generated. \n"
    print "config project in tomcat server.xml like :\n"
    print '    <Host name="virt.domain.com" appBase="webapps" unpackWARs="true" autoDeploy="true" xmlValidation="false" xmlNamespaceAware="false" />\n' 
    print 'config project in tomcat ${Tomcat_Base}\conf\Catalina\hector.kedou.com\ROOT.xml like:\n\n' \
          +'    <Context path="ROOT" reloadable="false" docBase="D:\work\demoapp\src\main\webapp" workDir="D:\work\demoapp\work" >\n'  \
          +'      <Loader className="org.apache.catalina.loader.DevLoader" reloadable="true" debug="1" useSystemClassLoaderAsParent="false" />\n' \
          +'    </Context>\n' \
