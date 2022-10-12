#coding=utf-8
import sys
import subprocess
 
 
path =  '~/ht_cloud_root'
##远程执行命令，此处执行Python.py文件
##可以替换任何在远程终端执行的命令。
remote_cmd = "cd /root/FinanceReportAnalysis && python /root/FinanceReportAnalysis/sinadata.py"
##参照ssh -i 命令编辑下面内容
ssh_cmd = "ssh " + "-i "+ path  + " root@82.157.52.106"  + remote_cmd
 
 
result = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 
 
buff = result.stdout.read()
print str(buff)