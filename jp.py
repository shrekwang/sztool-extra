import sys
from subprocess import Popen
from optparse import OptionParser 


if __name__ == "__main__" :

    description = " create mvn project based with 'shrek-archetype' archetype "
    usage="usage: jp -g groupId -i argifactId "
    parser = OptionParser(description = description, usage = usage)
    parser.add_option("--desc",action="store_true", dest="desc", default=False)
    parser.add_option('-g','--groupId', action="store", dest="groupId", default='org.wsn' )
    parser.add_option('-i','--artifactId', action="store", dest="artifactId", default='quick-test' )

    (options, args) = parser.parse_args()
    if options.desc :
        print parser.get_description()
        sys.exit(0)

    cmd_array = ["mvn archetype:generate",
            "-DarchetypeArtifactId=shrek-archetype",
            "-DinteractiveMode=false",
            "-DarchetypeGroupId=com.github.shrek",
            "-DarchetypeCatalog=local",
            "-DgroupId=%s -DartifactId=%s" ]
    cmd = " ".join(cmd_array)
    cmd = cmd % (options.groupId, options.artifactId)
    print cmd
    Popen(cmd,shell = True)
   

