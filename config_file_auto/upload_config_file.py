#!/usr/bin/env python
# -*- coding:utf-8 -*-
#时间：2018-10-27
#作者：Presley
#k8s上线脚本
import subprocess
import os, zipfile
from datetime import datetime
from config_file_auto.config.settings import *
from config_file_auto.config.ssh_tools import *


def make_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()

#make_zip("pymom","pymom.zip")

def up_local_config_file(project_id):
    online_host = "192.168.30.42"
    online_port = "22"
    online_user = "root"
    online_passwd = "123456"

    local_docker_host = "192.168.30.42"
    local_docker_port = "22"
    local_docker_user = "root"
    local_docker_passwd = "123456"
    # project_info = get_settings_info(project_id)
    # project_name = project_info['project_name']
    project_name = "k8stest-pymom"
    #压缩
    source_dir = "{project_name}".format(project_name = project_name)
    zip_file = "{project_name}.zip".format(project_name = project_name)
    make_zip(source_dir,zip_file)

    # 上传部署文件到本地服务器
    # local_project_file = "{project_name}.zip".format(project_name = project_name)
    # up_project_file = "/application/k8s-projects/{project_name}.zip".format(project_name = project_name)

    local_project_file = "{project_name}.zip".format(project_name = project_name)
    up_project_file = "/application/k8s-projects/{project_name}.zip".format(project_name = project_name)

    ssh_local = SshClient(local_docker_host, local_docker_port, local_docker_user, local_docker_passwd)
    ssh_local.up_file(local_project_file,up_project_file)
    jieya_cmd = "/usr/bin/unzip /application/k8s-projects/{project_name}.zip".format(project_name = project_name)
    ssh_local.exec_cmd(jieya_cmd)

    #;rm -rf /application/k8s-projects/{project_name}.zip
    #print("stdout is :" ,stdout, "stderr is :" ,stderr)
    ssh_local.close_connect()

    #上传docker compose文件到阿里云
    ssh_aliyun = SshClient(online_host, online_port, online_user, online_passwd)
    # #创建docker-compose目录
    # print("开始")
    ssh_aliyun.exec_cmd("mkdir -p /application/docker_hub/java/{project_name}".format(project_name = project_name))
    ssh_aliyun.up_file("./{project_name}/docker_compose_config/docker-compose-pro.zip".format(project_name=project_name), "/application/docker_hub/java/{project_name}/docker-compose-pro.zip".format(project_name=project_name))
    out1, out2 = ssh_aliyun.exec_cmd("cd /application/docker_hub/java/{project_name}/ && /usr/bin/unzip /application/docker_hub/java/{project_name}/docker-compose-pro.zip".format(project_name = project_name))
    print("out1:",out1.read().decode('utf-8'),out2)
    ssh_aliyun.close_connect()


if __name__ == "__main__":
    up_local_config_file(11)