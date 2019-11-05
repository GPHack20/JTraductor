import os
import subprocess
#print(os.popen("H:\\PROGRAMAS_WINDOWS\\cygwin64\\bin\\mintty.exe  -h always -e /bin/bash -l -c '/home/gsant/trans :ru Bonita -b'").read())
"""
command="H:\\PROGRAMAS_WINDOWS\\cygwin64\\bin\\mintty.exe  -h always -e /bin/bash -l -c '/home/gsant/trans :ru Bonita -b'"
"""
#command="bash -c '/home/gphack20/trans :ru \"La comida esta muy rica.\" -b'>>out.txt"
comando='"Nunca, jamas, ni con la rosa."'
os.system("bash -c '/home/gphack20/trans -b :ru {} '>out.txt".format(comando))

