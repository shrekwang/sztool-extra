from subprocess import Popen
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='jp {java project creator}: ')
    parser.add_argument('-g','--groupId', action="store", dest="groupId", default='org.wsn' )
    parser.add_argument('-i','--artifactId', action="store", dest="artifactId", default='quick-test' )
    return parser.parse_args()

if __name__ == "__main__" :

    args_info = parse_args()
    cmd_array = ["mvn archetype:generate",
            "-DarchetypeArtifactId=shrek-archetype",
            "-DinteractiveMode=false",
            "-DarchetypeGroupId=com.github.shrek",
            "-DarchetypeCatalog=local",
            "-DgroupId=%s -DartifactId=%s" ]
    cmd = " ".join(cmd_array)
    cmd = cmd % (args_info.groupId, args_info.artifactId)
    print cmd
    Popen(cmd,shell = True)
   

