import sys
import os.path
import os
from subprocess import Popen
from xml.etree.ElementTree import *

M2_REPO="d:/repo"
WORK_HOME="d:/work"

def getProjectClassPath():
    tree = ElementTree()
    classPathXmlPath = os.path.join(os.getcwd(), ".classpath")
    if not os.path.exists(classPathXmlPath):
        return None
    
    tree.parse(classPathXmlPath)
    entries = tree.findall("classpathentry")
    cp_entries = []
    for entry in  entries :
        if entry.get("kind") == "var" :
            path = entry.get("path")
            if "M2_REPO" in path:
                path = path.replace("M2_REPO",M2_REPO)
            path = os.path.normpath(path)
            cp_entries.append(path)
        if entry.get("kind") == "output" :
            path = os.path.normpath(os.path.join(os.getcwd(), entry.get("path")))
            cp_entries.append(path)

    return cp_entries

if __name__ == "__main__" :

    if len(sys.argv) != 2 :
        print "Usage: ngserver {start|stop}\n"
        sys.exit()

    opt = sys.argv[1]
    if opt == "start" :
        projectClassPath = getProjectClassPath()
        if projectClassPath == None :
            projectClassPath =[]
        projectClassPath.append(r"d:\soft\clojure-1.4.0\clojure-1.4.0.jar");
        projectClassPath.append(r"e:\github\clojure\vim\server-2.3.0.jar");
        cp = ";".join(projectClassPath)
        cmdline = r"java -cp %s vimclojure.nailgun.NGServer 127.0.0.1" % cp
        Popen(cmdline,shell = True)
    else :
        cmdline = "ng ng-stop"
        Popen(cmdline,shell = False)
